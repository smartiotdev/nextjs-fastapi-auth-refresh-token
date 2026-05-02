"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import toast from 'react-hot-toast';
import axios from 'axios';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';

import { REFRESH_TOKEN,ACCESS_TOKEN } from '@/constants';

interface User {
  id: number;
  email: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register:(email:string, password:string) =>Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType|undefined>(undefined)

export function AuthProvider({children}:{children:ReactNode}){
    const [user,setUser] = useState<User|null>(null)
    const[isLoading,setIsLoading] = useState(true)
    const router =useRouter()

    useEffect(()=>{
     const loadUser = async()=>{
        const token = localStorage.getItem(ACCESS_TOKEN)

        if(token){
            try {
                const {data} = await api.get('/users/me');
                setUser(data)
            } catch (error) {
                console.log("Err fetching the user data",error)
                localStorage.removeItem(ACCESS_TOKEN)
            }
        }
        setIsLoading(false)
     }
     loadUser()
    },[])
   
  const login = async (email: string, password: string) => {
    const { data } = await axios.post('http://localhost:8000/auth/login', { email, password });
    toast.success("User was successfully logged in!")
    localStorage.setItem(ACCESS_TOKEN, data.access_token);
    localStorage.setItem(REFRESH_TOKEN, data.refresh_token);

    const userResponse = await api.get('/users/me');
    setUser(userResponse.data);
    
    router.push('/dashboard');
  };

  //  The Smart Register Function
  const register = async (email: string, password: string) => {
    // Step 1: Create the account
    const res = await axios.post('http://localhost:8000/auth/register', { email, password });
    const{id} = res.data
    if(id){
     // Step 2: Auto-Login (The Combo Move)
     // We reuse the login function so we don't rewrite code
      await login(email, password); 
    }else{
       toast.error("User could not be registered!")
      }
  };
  const logout = ()=>{
    localStorage.removeItem(ACCESS_TOKEN)
    localStorage.removeItem(REFRESH_TOKEN)
    setUser(null)
    router.push('/dashboard')
  }

  return (
    <AuthContext.Provider value={{user,login,register,logout,isLoading}}>
        {children}
    </AuthContext.Provider>
  )

}


export const useAuth = ()=>{
    const context = useContext(AuthContext)
    if(!context) throw new Error("useAuth must be used within an AuthProvider");
    return context;
}