import {useState, useEffect} from 'react';
import {useRouter} from 'next/router';
import {login, register} from '@/auth_api/api';
import {UserSchema} from './schemes';
import styles from '@/styles/auth/AuthForm.module.scss';
import CheckEmailAnimation from '@/auth_api/animations';

const AuthForm = ({isLogin}) => {
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showEmailCheck, setShowEmailCheck] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [isButtonDisabled, setIsButtonDisabled] = useState(false);
    const router = useRouter();
    const userData = {first_name, last_name, email, password};


    const handleRegSubmit = async (e) => {
        e.preventDefault();
        setErrorMessage('');
        try {
            await register(userData);
            setIsButtonDisabled(true);
            setTimeout(() => setIsButtonDisabled(false), 60000);
            setShowEmailCheck(true);
        } catch (error) {
            setShowEmailCheck(false);
            if (error.response?.status === 400 &&
                error.response?.data?.message === "User authorized") {
                setErrorMessage('Пользователь зарегистрирован');
            } else {
                setErrorMessage('Ошибка при регистрации. Попробуйте снова.');
            }
        }
    };

    const handleLogSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(userData);
            router.push('/');
        } catch (error) {
            if (error.response?.status === 400 &&
                error.response?.data?.message === "invalid email or password") {
                setErrorMessage('Неверный email или пароль.');
            } else if (error.response?.status === 400 &&
                error.response?.data?.message === "user auth in system") {
                setErrorMessage('Пользователь уже зарегистрирован через google.');
            } else {
                setErrorMessage('Ошибка при входе в аккаунт. Попробуйте снова');
            }
        }
    };

    useEffect(() => {
        setErrorMessage('');
        setShowEmailCheck(false);
    }, [isLogin]);

    return (
        <div className={styles.container}>
            <form onSubmit={isLogin ? handleLogSubmit : handleRegSubmit} className={styles.form}>
                <h2 className={styles.title}>{isLogin ? 'Вход' : 'Регистрация'}</h2>
                {!isLogin && (
                    <input
                        className={styles.input}
                        type="text"
                        placeholder="Имя"
                        value={first_name}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                    />


                )}
                {!isLogin && (
                    <input
                        className={styles.input}
                        type="text"
                        placeholder="Фамилия"
                        value={last_name}
                        onChange={(e) => setLastName(e.target.value)}
                        required
                    />

                )}

                <input
                    className={styles.input}
                    type="email"
                    placeholder="Почта"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    className={styles.input}
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <br/>
                <button type="submit" className={styles.button} disabled={isButtonDisabled}>
                    {isLogin ? 'Вход' : 'Регистрация'}
                </button>



                {errorMessage && <div className={styles.errorMessage}>{errorMessage}</div>}
                <div className={styles.linksContainer}>
                    <a href='/forgot-password' className={styles.link}>Забыл пароль</a>
                    <a href={isLogin ? '/registration' : '/login'} className={styles.link}>
                        {isLogin ? 'Нет аккаунта' : 'Уже зарегистрирован'}
                    </a>
                </div>
            </form>
            {!errorMessage && showEmailCheck && <CheckEmailAnimation onClose={() => setShowEmailCheck(false)}/>}
        </div>
    );
};

export default AuthForm;