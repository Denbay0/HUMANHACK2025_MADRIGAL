import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // добавляем BrowserRouter и Routes
import './index.css';
import App from './landing/App.jsx';            // Главная страница
import Login from './login/pass.jsx';            // Страница логина/регистрации
import ProfileApp from './profile/App_profile.jsx';        // Профиль (из App_profile.jsx)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />            {/* Главная страница */}
        <Route path="/login" element={<Login />} />       {/* Страница логина */}
        <Route path="/profile" element={<ProfileApp />} />  {/* Страница профиля */}
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
