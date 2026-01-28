export default function Unauthorized() {
    return (
        <div className="h-screen flex items-center justify-center text-center">
            <div>
                <h1 className="text-2xl font-bold">Not authorized</h1>
                <p className="text-gray-500 mt-2">
                    You are not authorized to access this site.<br />
                    Please get in touch with the organizer to register.
                </p>

                <button className="bg-white text-black font-bold p-3 rounded-lg cursor-pointer font-mono m-5 hover:bg-gray-100 active:bg-gray-300">
                    Register as admin
                </button>
            </div>
        </div>
    );
}
  