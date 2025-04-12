import React, { useState, useEffect } from "react";
import './App_prof.css';

const getUserIdFromLocalStorage = () => {
  const userId = localStorage.getItem("userId");
  if (userId) {
    console.log("User ID found in localStorage:", userId);
    return parseInt(userId, 10);
  } else {
    console.error("User ID not found in localStorage");
    return null;
  }
};

function EditProfileModal({ user, onClose, onSave, onDelete }) {
  const initialFormState = {
    firstName: user?.firstName || "",
    lastName: user?.lastName || "",
    email: user?.email || "",
    username: user?.username || "",
    timezone: user?.timezone || "UTC+3:00"
  };

  const [formData, setFormData] = useState(initialFormState);
  const [isPasswordTab, setIsPasswordTab] = useState(false);
  const [passwordData, setPasswordData] = useState({
    oldPassword: "",
    newPassword: "",
    confirmNewPassword: "",
  });

  useEffect(() => {
    setFormData(initialFormState);
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmitProfile = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleSubmitPasswordChange = async (e) => {
    e.preventDefault();

    if (passwordData.newPassword !== passwordData.confirmNewPassword) {
      alert("Новый пароль и подтверждение не совпадают.");
      return;
    }

    try {
      const checkResponse = await fetch('http://localhost:8000/auth/check-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: user.username,
          oldPassword: passwordData.oldPassword,
        }),
      });

      const checkData = await checkResponse.json();
      if (!checkResponse.ok) {
        throw new Error(checkData.error || 'Не удалось проверить пароль');
      }

      const updateResponse = await fetch('http://localhost:8000/auth/update-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: user.username,
          newPassword: passwordData.newPassword,
        }),
      });

      const updateData = await updateResponse.json();
      if (!updateResponse.ok) {
        throw new Error(updateData.error || 'Не удалось обновить пароль');
      }

      alert('Пароль успешно изменён');
      setPasswordData({
        oldPassword: "",
        newPassword: "",
        confirmNewPassword: "",
      });
    } catch (error) {
      console.error("Ошибка при изменении пароля:", error);
      alert(error.message || "Ошибка при изменении пароля");
    }
  };

  const handleReset = () => {
    setFormData(initialFormState);
  };

  const handleChangeTab = () => {
    setIsPasswordTab(prev => !prev);
  };

  const timezones = [
    "UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-9:00", "UTC-8:00",
    "UTC-7:00", "UTC-6:00", "UTC-5:00", "UTC-4:00", "UTC-3:00",
    "UTC-2:00", "UTC-1:00", "UTC±0:00", "UTC+1:00", "UTC+2:00",
    "UTC+3:00", "UTC+4:00", "UTC+5:00", "UTC+6:00", "UTC+7:00",
    "UTC+8:00", "UTC+9:00", "UTC+10:00", "UTC+11:00", "UTC+12:00"
  ];

  return (
    <div className="modal-overlay show">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Редактирование профиля</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-tabs">
          <button onClick={handleChangeTab} className={isPasswordTab ? "active" : ""}>
            Сменить пароль
          </button>
          <button onClick={handleChangeTab} className={!isPasswordTab ? "active" : ""}>
            Создать новый сервер
          </button>
        </div>

        {isPasswordTab ? (
          <form onSubmit={handleSubmitPasswordChange}>
            <div className="form-group">
              <label>Старый пароль:</label>
              <input
                type="password"
                name="oldPassword"
                value={passwordData.oldPassword}
                onChange={handlePasswordChange}
              />
            </div>
            <div className="form-group">
              <label>Новый пароль:</label>
              <input
                type="password"
                name="newPassword"
                value={passwordData.newPassword}
                onChange={handlePasswordChange}
              />
            </div>
            <div className="form-group">
              <label>Подтвердите новый пароль:</label>
              <input
                type="password"
                name="confirmNewPassword"
                value={passwordData.confirmNewPassword}
                onChange={handlePasswordChange}
              />
            </div>
            <div className="modal-actions">
              <button type="submit" className="save-btn">Сменить пароль</button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleSubmitProfile}>
            <div className="form-group">
              <label>Имя:</label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Фамилия:</label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Логин:</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                disabled
              />
            </div>
            <div className="form-group">
              <label>Часовой пояс:</label>
              <select
                name="timezone"
                value={formData.timezone}
                onChange={handleChange}
              >
                {timezones.map(tz => (
                  <option key={tz} value={tz}>{tz}</option>
                ))}
              </select>
            </div>
            <div className="modal-actions">
              <button type="submit" className="save-btn">Сохранить изменения</button>
              <button type="button" className="reset-btn" onClick={handleReset}>Сбросить</button>
              <button type="button" className="delete-btn" onClick={onDelete}>Удалить профиль</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

function Profile({ user, servers, isLoading, onEditProfile }) {
  return (
    <div className="profile">
      {isLoading ? (
        <p>Загрузка данных...</p>
      ) : (
        <>
          <h2 className="users">{user.firstName} {user.lastName}</h2>
          <p className="mail">{user.email}</p>
          <div className="servers-container">
            <div className="profile-actions">
              <button className="edit-profile-btn" onClick={onEditProfile}>
                Создать новый сервер
              </button>
            </div>
            <h3 className="servers-title">Мои серверы</h3>
            {servers.length > 0 ? (
              <div className="servers-list">
                {servers.map(server => (
                  <div key={server.id} className={`server-card ${server.isActive ? 'online' : 'offline'}`}>
                    <h4 className="server-name">{server.name}</h4>
                    <div className="server-specs">
                      <div className="spec-item">
                        <span className="spec-label">CPU:</span> {server.cpu}
                      </div>
                      <div className="spec-item">
                        <span className="spec-label">RAM:</span> {server.ram}
                      </div>
                      <div className="spec-item">
                        <span className="spec-label">Storage:</span> {server.storage}
                      </div>
                      <div className="spec-item">
                        <span className="spec-label">Price:</span> {server.price}
                      </div>
                    </div>
                    <div className={`server-status ${server.isActive ? 'online' : 'offline'}`}>
                      {server.isActive ? '🟢 Online' : '🔴 Offline'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-servers">У вас нет серверов</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

function App() {
  const initialUserId = getUserIdFromLocalStorage();
  console.log("Initial user id from localStorage:", initialUserId);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState({
    id: initialUserId,
    firstName: "Влад",
    lastName: "Афонин",
    email: "afonin@example.com",
    username: "afonin.vlad",
    timezone: "UTC+3:00"
  });
  const [servers, setServers] = useState([]);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const fetchServers = async () => {
      try {
        console.log("Fetching servers for user id:", user.id);
        const jwt = localStorage.getItem("token");
        const response = await fetch(`http://localhost:8000/users/${user.id}/servers?jwt_token=${encodeURIComponent(jwt)}`);
        if (response.ok) {
          const data = await response.json();
          console.log("Servers data received:", data);
          const allServers = Object.values(data).flat();
          setServers(allServers);
        } else {
          console.error("Ошибка загрузки серверов, статус", response.status);
        }
      } catch (error) {
        console.error("Ошибка загрузки серверов:", error);
      } finally {
        setIsLoading(false);
      }
    };

    if (user && user.id) {
      fetchServers();
    } else {
      setIsLoading(false);
    }
  }, [user.id]);

  const handleEditProfile = () => {
    setIsEditing(true);
  };

  const handleSaveProfile = async (updatedUser) => {
    try {
      setUser(updatedUser);
      setIsEditing(false);
      alert("Изменения сохранены!");
    } catch (error) {
      console.error("Ошибка сохранения:", error);
      alert("Ошибка при сохранении изменений");
    }
  };

  const handleDeleteProfile = () => {
    if (window.confirm("Вы уверены, что хотите удалить профиль?")) {
      setUser({
        id: null,
        firstName: "",
        lastName: "",
        email: "",
        username: "",
        timezone: ""
      });
      setIsEditing(false);
      alert("Профиль удалён");
    }
  };

  return (
    <main className="body">
      <div className="container">
        <div className="cub"></div>
        <h1 className="name">ServerLink</h1>
        <hr className="line" />
        <Profile
          user={user}
          servers={servers}
          isLoading={isLoading}
          onEditProfile={handleEditProfile}
        />
        {isEditing && (
          <EditProfileModal
            user={user}
            onClose={() => setIsEditing(false)}
            onSave={handleSaveProfile}
            onDelete={handleDeleteProfile}
          />
        )}
      </div>
    </main>
  );
}

export default App;
