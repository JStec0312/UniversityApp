import "./globals.css";
import {UserProvider} from "./UserContext";
import { AdminProvider } from "./AdminContext";

export default function RootLayout({ children }) {

  return (
    <html lang="pl">
      <body>
        <UserProvider>
          <AdminProvider>
            {children}
          </AdminProvider>
        </UserProvider>
      </body>
    </html>
  );
}