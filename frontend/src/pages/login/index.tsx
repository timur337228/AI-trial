import HomeAuth from '@/auth_api/schemes';
import Home,  from '@/auth_api/render';
import { getServerSideProps } from '@/auth_api/render';
import React from "react";

export const loginUser: React.FC<HomeAuth> = ({user}) => {
    return <Home user={user} isLogin={true}></Home>;
}
export { getServerSideProps };
export default loginUser;