import React, { useState } from 'react';
import './password.css';

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const toggleForm = () => {
    setError('');
    setIsLogin(!isLogin);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        if (data.detail && Array.isArray(data.detail) && data.detail.length) {
          setError(data.detail[0].msg);
        } else if (typeof data.detail === 'string') {
          setError(data.detail);
        } else {
          setError(JSON.stringify(data));
        }
      } else {
        localStorage.setItem("token", data.access_token);
        if (data.user_id) {
          localStorage.setItem("userId", data.user_id);
        } else {
          console.warn("User ID не получен от сервера");
        }
        window.location.href = "/profile";
      }
    } catch (err) {
      console.error("Ошибка при логине:", err);
      setError("Ошибка подключения к серверу");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        if (data.detail && Array.isArray(data.detail) && data.detail.length) {
          setError(data.detail[0].msg);
        } else if (typeof data.detail === 'string') {
          setError(data.detail);
        } else {
          setError(JSON.stringify(data));
        }
      } else {
        setIsLogin(true);
        setError('');
      }
    } catch (err) {
      console.error("Ошибка при регистрации:", err);
      setError("Ошибка подключения к серверу");
    }
  };

  return (
    <div className="main">
      <input
        type="checkbox"
        id="chk"
        aria-hidden="true"
        checked={!isLogin}
        onChange={toggleForm}
      />
      <div className="signup">
        <form onSubmit={handleRegister}>
          <label htmlFor="chk" aria-hidden="true">Регистрация</label>
          <input
            type="text"
            name="username"
            placeholder="Имя пользователя"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Пароль"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Зарегистрироваться</button>
        </form>
      </div>
      <div className="login">
        <form onSubmit={handleLogin}>
          <label htmlFor="chk" aria-hidden="true">Вход</label>
          <input
            type="text"
            name="username"
            placeholder="Имя пользователя"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Пароль"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Вход</button>
        </form>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
}

export default AuthPage;
