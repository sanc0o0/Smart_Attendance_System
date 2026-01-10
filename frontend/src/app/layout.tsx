import "./globals.css";
import { Toaster } from "react-hot-toast";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: "#111",
              color: "#fff",
            },
          }}
        />
      </body>
    </html>
  );
}
