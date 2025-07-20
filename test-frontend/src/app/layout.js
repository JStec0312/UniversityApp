import "./globals.css";
import {UserProvider} from "./UserContext";

export default function RootLayout({ children }) {

  return (
    <html lang="pl">
      <body>
        <UserProvider>
            {children}
        </UserProvider>
      </body>
    </html>
  );
}