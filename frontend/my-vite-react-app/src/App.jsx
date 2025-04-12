
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import myImage from './assets/uwu.svg';
import people from './assets/lol.svg';

function App() {
  const elementsRef = useRef([]);
  const [visibleElements, setVisibleElements] = useState({});
  const navigate = useNavigate(); // добавили навигатор для маршрутизации

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const index = elementsRef.current.findIndex(el => el === entry.target);
            if (index !== -1) {
              setVisibleElements(prev => ({
                ...prev,
                [index]: true
              }));
            }
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );

    elementsRef.current.forEach(el => {
      if (el) observer.observe(el);
    });

    return () => {
      elementsRef.current.forEach(el => {
        if (el) observer.unobserve(el);
      });
    };
  }, []);

  const getAnimatedStyle = (index) => {
    return visibleElements[index] ? {
      opacity: 1,
      transform: 'translateY(0)',
      transition: 'opacity 0.6s ease-out, transform 0.6s ease-out'
    } : {
      opacity: 0,
      transform: 'translateY(20px)',
      transition: 'opacity 0.6s ease-out, transform 0.6s ease-out'
    };
  };

  return (
    <main className='body'>
      <div className='container'>
        <div ref={el => elementsRef.current[0] = el} className='cub' style={getAnimatedStyle(0)} />

        <h1 ref={el => elementsRef.current[1] = el} className='name' style={getAnimatedStyle(1)}>
          ServerLink
        </h1>

        <button
          ref={el => elementsRef.current[2] = el}
          className='log'
          style={getAnimatedStyle(2)}
          onClick={() => navigate('/login')} // переход на страницу логина
        >
          зарегистрироваться / войти
        </button>

        <hr ref={el => elementsRef.current[3] = el} className='line' style={getAnimatedStyle(3)} />

        <h2 ref={el => elementsRef.current[4] = el} className='time' style={getAnimatedStyle(4)}>
          Ваше время – наш приоритет
        </h2>

        <p ref={el => elementsRef.current[5] = el} className='uwu' style={getAnimatedStyle(5)}>
          Разверните свой проект в интернете всего за несколько минут с помощью интуитивно понятной панели управления.<br /><br />
          Мы убеждены, что даже самые сложные технологии должны быть простыми в использовании. Наша задача – минимизировать рутинные настройки, чтобы вы могли сосредоточиться на развитии бизнеса.<br /><br />
          Благодаря глубокой интеграции всех сервисов, вы сможете быстро развернуть инфраструктуру для любых задач – от личного блога до высоконагруженного приложения.
        </p>

        <img ref={el => elementsRef.current[6] = el} className='setu' src={myImage} alt="Server illustration" style={getAnimatedStyle(6)} />

        <h2 ref={el => elementsRef.current[7] = el} className='tex' style={getAnimatedStyle(7)}>
          Надежная техническая поддержка
        </h2>

        <p ref={el => elementsRef.current[8] = el} className='xz' style={getAnimatedStyle(8)}>
          Экспертная помощь Подберем оптимальное решение под ваши задачи. В большинстве случаев решаем вопросы без необходимости перехода на более дорогой тариф.<br /><br />
          Только реальные люди Никаких бездушных ботов – наши специалисты всегда на связи и готовы помочь.<br /><br />
          Мгновенная реакция Мы ценим ваше время, поэтому разместили контакты поддержки на видном месте. Обращайтесь – поможем без задержек!<br /><br />
          Гарантия оперативности С какой бы проблемой вы ни столкнулись – мы оперативно отреагируем и найдем решение.
        </p>

        <img ref={el => elementsRef.current[9] = el} className='foto' src={people} alt="Support team" style={getAnimatedStyle(9)} />


        <hr
          ref={el => elementsRef.current[10] = el}
          className='line2'
          style={getAnimatedStyle(10)}
        />

        <h2
          ref={el => elementsRef.current[11] = el}
          className='kak'
          style={getAnimatedStyle(11)}
        >
          Как арендовать сервер на ServerLink
        </h2>

        <p
          ref={el => elementsRef.current[12] = el}
          className='arenda'
          style={getAnimatedStyle(12)}
        >
          Аренда сервера в ServerLink — это быстрый и удобный процесс. Всего несколько шагов, и ваш проект будет готов к работе!
        </p>

        <hr
          ref={el => elementsRef.current[13] = el}
          className='line3'
          style={getAnimatedStyle(13)}
        />

        <div
          ref={el => elementsRef.current[14] = el}
          className='one'
          style={getAnimatedStyle(14)}
        />

        <p
          ref={el => elementsRef.current[15] = el}
          className='te'
          style={getAnimatedStyle(15)}
        >
          1. Выберите тип сервера.<br /><br />
          На ServerLink доступны:<br /> VPS — виртуальные серверы с гибкой настройкой <br /> Выделенные серверы — максимальная производительность <br />Облачные решения — масштабируемые ресурсы
        </p>

        <div
          ref={el => elementsRef.current[16] = el}
          className='two'
          style={getAnimatedStyle(16)}
        />

        <p
          ref={el => elementsRef.current[17] = el}
          className='z'
          style={getAnimatedStyle(17)}
        >
          2. Настройте конфигурацию<br /><br />
          Выберите параметры:<br /> Операционная система (Ubuntu, CentOS, Debian, Windows) <br />Процессор (CPU) — от 1 до 32 ядер<br /> Оперативная память (RAM) — от 1 ГБ до 128 ГБ <br /> Диск (SSD/NVMe) — от 10 ГБ до 2 ТБ <br /> Доп. опции (DDoS-защита, резервные копии)
        </p>

        <p
          ref={el => elementsRef.current[18] = el}
          className='covet'
          style={getAnimatedStyle(18)}
        >
          Совет: Если не уверены в выборе – начните с минимальной конфигурации, ресурсы можно увеличить в любой момент.
        </p>

        <div
          ref={el => elementsRef.current[19] = el}
          className='three'
          style={getAnimatedStyle(19)}
        />

        <p
          ref={el => elementsRef.current[20] = el}
          className='oformite'
          style={getAnimatedStyle(20)}
        >
          3. Оформите заказ<br /><br />
          Нажмите «Заказать»<br />
          Выберите срок аренды (чем дольше, тем выгоднее).<br />
          Оплатите удобным способом: Карта (Visa/Mastercard/Мир)<br /> Банковский перевод<br /> Криптовалюта (Bitcoin, USDT)
        </p>

        <div
          ref={el => elementsRef.current[21] = el}
          className='doctyn'
          style={getAnimatedStyle(21)}
        />

        <p
          ref={el => elementsRef.current[22] = el}
          className='server'
          style={getAnimatedStyle(22)}
        >
          4. Получите доступ к серверу<br /><br />
          Мгновенная активация (1-2 минуты после оплаты).<br />Данные для входа придут на почту:<br />
          IP-адрес сервера<br />
          Логин и пароль (или SSH-ключ)<br />
          Ссылка на панель управления
        </p>

        <div
          ref={el => elementsRef.current[23] = el}
          className='four'
          style={getAnimatedStyle(23)}
        />

        <p
          ref={el => elementsRef.current[24] = el}
          className='work'
          style={getAnimatedStyle(24)}
        >
          5. Начните работать<br /><br />
          Подключитесь к серверу:<br />Через SSH (используя Terminal, PuTTY или встроенный веб-терминал ServerLink).<br />Через панель управления — мониторинг<br /> ресурсов, установка ПО, управление файлами.
        </p>
      </div>
    </main>
  );
}

export default App;