import { useNavigate } from 'react-router-dom';
import './App.css';
import myImage from './assets/uwu.svg';
import people from './assets/lol.svg';

function App() {
  const navigate = useNavigate();

  const staticStyle = {
    opacity: 1,
    transform: 'translateY(0)',
    transition: 'opacity 0.6s ease-out, transform 0.6s ease-out'
  };

  return (
    <main className="body">
      <div className="container">
        <div className="cub" style={staticStyle} />

        <h1 className="name" style={staticStyle}>
          ServerLink
        </h1>

        <button
          className="log"
          style={staticStyle}
          onClick={() => navigate('/login')}
        >
          зарегистрироваться / войти
        </button>

        <hr className="line" style={staticStyle} />

        <h2 className="time" style={staticStyle}>
          Ваше время – наш приоритет
        </h2>

        <p className="uwu" style={staticStyle}>
          Разверните свой проект в интернете всего за несколько минут с помощью интуитивно понятной панели управления.
          <br /><br />
          Мы убеждены, что даже самые сложные технологии должны быть простыми в использовании. Наша задача – минимизировать рутинные настройки, чтобы вы могли сосредоточиться на развитии бизнеса.
          <br /><br />
          Благодаря глубокой интеграции всех сервисов, вы сможете быстро развернуть инфраструктуру для любых задач – от личного блога до высоконагруженного приложения.
        </p>

        <img
          className="setu"
          src={myImage}
          alt="Server illustration"
          style={staticStyle}
        />

        <h2 className="tex" style={staticStyle}>
          Надежная техническая поддержка
        </h2>

        <p className="xz" style={staticStyle}>
          Экспертная помощь Подберем оптимальное решение под ваши задачи. В большинстве случаев решаем вопросы без необходимости перехода на более дорогой тариф.
          <br /><br />
          Только реальные люди, никаких бездушных ботов – наши специалисты всегда на связи и готовы помочь.
          <br /><br />
          Мгновенная реакция: мы ценим ваше время, поэтому разместили контакты поддержки на видном месте. Обращайтесь – поможем без задержек!
          <br /><br />
          Гарантия оперативности: с какой бы проблемой вы ни столкнулись – мы оперативно отреагируем и найдем решение.
        </p>

        <img
          className="foto"
          src={people}
          alt="Support team"
          style={staticStyle}
        />

        <hr className="line2" style={staticStyle} />

        <h2 className="kak" style={staticStyle}>
          Как развернуть сервер на ServerLink
        </h2>

        <p className="arenda" style={staticStyle}>
          Развертывание сервера на ServerLink — это быстрый и автоматизированный процесс, который займет всего несколько минут. Вот как это работает:
        </p>

        <hr className="line3" style={staticStyle} />

        <div className="one" style={staticStyle} />

        <p className="te" style={staticStyle}>
          1. – VPS – легкие виртуальные серверы с быстрым запуском <br /><br />
          – Выделенные серверы – мощные физические машины для ресурсоемких задач<br /><br />
          – Облачные кластеры – масштабируемые решения для высоконагруженных проектов
        </p>

        <div className="two" style={staticStyle} />

        <p className="z" style={staticStyle}>
          2. – После оплаты сервер автоматически активируется (1-2 минуты)<br /><br /> 
          – Система самостоятельно настраивает ОС, сеть и базовое окружение<br /><br /> 
          – Доступные ОС: Ubuntu, Debian, CentOS, Windows Server
        </p>

        <p className="covet" style={staticStyle}>
          Совет: Если не уверены в выборе – начните с минимальной конфигурации, ресурсы можно увеличить в любой момент.
        </p>

        <div className="three" style={staticStyle} />

        <p className="oformite" style={staticStyle}>
          3. – На ваш email придут:<br /><br /> 
          - IP-адрес сервера<br /><br /> 
          - Логин и пароль (или SSH-ключ)<br /><br /> 
          - Ссылка на веб-панель управления<br /><br /> 
          – Можно сразу подключаться через SSH, RDP или веб-консоль
        </p>

        <div className="doctyn" style={staticStyle} />

        <p className="server" style={staticStyle}>
          4. – Установите нужное ПО (Docker, Nginx, MySQL и др.)<br /><br /> 
          – Настройте брандмауэр и безопасность<br /><br /> 
          – Загрузите файлы проекта и запускайте свои сервисы
        </p>

        <div className="four" style={staticStyle} />

        <p className="work" style={staticStyle}>
          5. ServerLink обеспечивает стабильную работу без ручных настроек <br /> — просто выберите сервер и начинайте работать!
        </p>
      </div>
    </main>
  );
}

export default App;
