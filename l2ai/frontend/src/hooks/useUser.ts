// import { useContext } from "react";
// import AuthContext from "../context/authContext";
// import useLocalStorage from "./useLocalStorage";
// import { IUser } from "../interfaces";


// const useUser = () => {
//   const {
//     user,
//     setUser,
//     isAuthenticated,
//     setIsAuthenticated,
//     accessToken,
//     setAccessToken,
//     refreshToken,
//     setRefreshToken
//   } = useContext(AuthContext);

//   const { setItem } = useLocalStorage();

//   const addUser = (user: IUser) => {
//     setUser(user);
//     setIsAuthenticated(true);
//     setAccessToken(user.accessToken);
//     setRefreshToken(user.refreshToken);
//     setItem("user", JSON.stringify(user));
//   };

//   const removeUser = () => {
//     setUser(null);
//     setIsAuthenticated(false);
//     setAccessToken("");
//     setRefreshToken("");
//     setItem("user", "");
//   };

//   return {
//     user,
//     addUser,
//     removeUser,
//     setUser,
//     isAuthenticated,
//     setIsAuthenticated,
//     accessToken,
//     setAccessToken,
//     refreshToken,
//     setRefreshToken
//   };
// };


// export default useUser;
