import ImageWithFallback from '@/app/components/ImageFallback';
import Settings from '@/app/components/Settings';
import userFallbackImage from '../../../../../public/default_user.svg'

export default async function ProfilePageId({ params }: { params: { id: string } }) {
  const { id } = params;
  let photoApiURL = '';
  let userApiURL = '';
  let name = "User Not Found";

  userApiURL = `${process.env.BACKEND_SERVER_USER_SERVICE?? "http://localhost:8000"}/api/v1/user/${id}`;
  photoApiURL = `${process.env.BACKEND_SERVER_IMAGE_STORAGE_SERVICE?? "http://localhost:8003"}/api/v1/photo/${id}`;

  try {
    const [user_promise, photo_promise] = await Promise.allSettled([
      fetch(userApiURL),
      fetch(photoApiURL),
    ]);

    const userResult = user_promise.status === 'fulfilled' && user_promise.value.status == 200 ? await user_promise.value.json() : null;
    const photoResult = photo_promise.status === 'fulfilled' && photo_promise.value.status == 200 ? await photo_promise.value.json() : null;

    name = userResult?.username.split("#")[0] || "User Not Found";
    const photo_url = photoResult as string;

    return (
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex justify-center">
            <div className="w-32 h-32 rounded-full overflow-hidden">
              <ImageWithFallback src={photo_url} alt={`Photo of ${name}`} fallback={userFallbackImage.src} />
            </div>
          </div>
          <div className="text-center mt-4">
            <h1 className="text-2xl font-bold text-black">{name}</h1>
          </div>
          <Settings id={params.id} />
        </div>
      </div>
    );
  } catch (error: any) {
    if (error.cause?.code === "ECONNREFUSED") {
      console.error(
        "Error connecting to backend API. Is backend service working?"
      )
    } else {
      console.error(
        error
      )
    }
  }
}
