import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // добавляем BrowserRouter и Routes
import './index.css';
import App from './landing/App.jsx';
import Login from './login/pass.jsx'; 
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter> {/* Оборачиваем всё в BrowserRouter */}
      <Routes> {/* Указываем маршруты */}
        <Route path="/" element={<App />} /> {/* Главная страница */}
        <Route path="/login" element={<Login />} /> {/* Страница логина */}
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
