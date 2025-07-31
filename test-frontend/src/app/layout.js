import "./globals.css";
import {UserProvider} from "./context/UserContext";
import { AdminProvider } from "./context/AdminContext";
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