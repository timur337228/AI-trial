import {TokenInfo} from "@/auth_api/schemes";
import {getIsLoginUser} from "@/auth_api/api"

export const isAuthenticated = async (): Promise<boolean> => {
    try {
        await getIsLoginUser();
        return true
    } catch {
        return false;
    }
};
