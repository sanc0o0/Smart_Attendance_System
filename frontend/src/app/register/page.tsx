export default function RegisterPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-black text-white">
            <div className="max-w-md text-center space-y-4">
                <h1 className="text-2xl font-bold">Registration</h1>
                <p className="text-gray-400">
                    This system is restricted.
                    <br />
                    Please contact the organizer to get access.
                </p>

                <div className="bg-neutral-900 p-4 rounded-xl text-left">
                    <p>Email: <span className="text-blue-400">admin@test.com</span></p>
                    <p>Institute: XYZ College</p>
                </div>
            </div>
        </div>
    );
}
  