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
      {/* Переключатель между формами */}
      <input
        type="checkbox"
        id="chk"
        aria-hidden="true"
        checked={!isLogin}
        onChange={toggleForm}
      />

      {/* Форма регистрации */}
      <div className="signup">
        <form onSubmit={handleRegister}>
          <label htmlFor="chk" aria-hidden="true">Sign up</label>
          <input
            type="text"
            name="username"
            placeholder="User name"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Sign up</button>
        </form>
      </div>

      {/* Форма логина */}
      <div className="login">
        <form onSubmit={handleLogin}>
          <label htmlFor="chk" aria-hidden="true">Login</label>
          <input
            type="text"
            name="username"
            placeholder="User name"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Login</button>
        </form>
        {/* Вывод ошибки */}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
}

export default AuthPage;
