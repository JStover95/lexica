import { Outlet } from "react-router-dom";


/**
 * The React Router layout for all children of the login component.
 */
const LoginLayout = () => {
  return (
    <main className="wrapper">
      <div className="container">
        <div className="column p2 grow align-center">
          <div className="mb2">
            <h1>Lexica</h1>
          </div>
          <Outlet />
        </div>
      </div>
    </main>
  );
};


export default LoginLayout;
