import AuthForm from '@/auth_api/authForm';
import {GetServerSideProps} from 'next';
import HomeAuth, {UserSchema} from '@/auth_api/schemes';
import {getCurrentUser} from '@/auth_api/api';
import React, {useEffect} from "react";
import {useRouter} from 'next/router'
import HomeProps from "@/auth_api/schemes";



const Home: React.FC<HomeAuth> = ({user, isLogin = true}) => {
    const router = useRouter();
    // useEffect(() => {
    //     if (!user) {
    //         router.push('/');
    //     }
    // }, [user, router]);
    // if (!user){
    //     return null;
    return (<div>
            <AuthForm isLogin={isLogin}/>
        </div>
    );

};


export const getServerSideProps: GetServerSideProps<HomeProps> = async (context) => {
    const {req} = context;
    const accessToken = req.headers.accessToken;

    if (!accessToken) {
        return {
            props: {
                user: null,
            },
        };
    }

    const user = await getCurrentUser();
    return {
        props: {
            user,
        },
    };

};


export default Home;