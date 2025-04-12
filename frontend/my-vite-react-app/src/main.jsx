import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './landing/App.jsx';
import Login from './login/pass.jsx';
import ProfileApp from './profile/App_profile.jsx';
import TerminalPage from './terminal/TerminalPage.jsx';
import TerminalTest from './terminal/TerminalTest.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<ProfileApp />} />
        <Route path="/terminal" element={<TerminalPage />} />
        <Route path="/test" element={<TerminalTest />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
