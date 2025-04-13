import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './landing/App.jsx';            // Главная страница (публичная)
import Login from './login/pass.jsx';             // Страница авторизации (публичная)
import ProfileApp from './profile/App_profile.jsx'; // Профиль пользователя (защищён)
import TerminalPage from './terminal/TerminalPage.jsx'; // Страница подключения к SSH (защищённая)
import TerminalWindow from './terminal/TerminalWindow.jsx'; // SSH-терминал (защищённая)
import RDPPage from './terminal/RDPPage.jsx';       // Страница подключения по RDP (защищённая)
import ProtectedRoute from "./ProtectedRoute.jsx";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        
        {/* Защищённые маршруты */}
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfileApp />
            </ProtectedRoute>
          }
        />
        <Route
          path="/terminal"
          element={
            <ProtectedRoute>
              <TerminalPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/terminal/:sessionId"
          element={
            <ProtectedRoute>
              <TerminalWindow />
            </ProtectedRoute>
          }
        />
        <Route
          path="/rdp"
          element={
            <ProtectedRoute>
              <RDPPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
