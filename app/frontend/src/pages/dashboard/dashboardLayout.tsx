import { Outlet } from "react-router-dom";


const DashboardLayout = () => {
  return (
    <main className="wrapper">
      <div className="container">
        <div className="column grow align-center">
          <div>
            <h1>Lexica</h1>
          </div>
          <div className="flex w100p">
            <Outlet />
          </div>
        </div>
      </div>
    </main>
  );
};


export default DashboardLayout;
