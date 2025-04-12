
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import myImage from './assets/uwu.svg';
import people from './assets/lol.svg';

function App() {
  const elementsRef = useRef([]);
  const [visibleElements, setVisibleElements] = useState({});
  const navigate = useNavigate();

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
          onClick={() => navigate('/login')}
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
          Как развернуть сервер на ServerLink
        </h2>

        <p
          ref={el => elementsRef.current[12] = el}
          className='arenda'
          style={getAnimatedStyle(12)}
        >
          Развертывание сервера на ServerLink — это быстрый и автоматизированный процесс, который займет всего несколько минут. Вот как это работает:
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
          1. – VPS – легкие виртуальные серверы с быстрым запуском <br /> <br />
– Выделенные серверы – мощные физические машины для ресурсоемких задач<br /><br />
– Облачные кластеры – масштабируемые решения для высоконагруженных проектов
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
          2. – После оплаты сервер автоматически активируется (1-2 минуты)<br /> <br /> 
– Система самостоятельно настраивает ОС, сеть и базовое окружение<br /> <br /> 
– Доступные ОС: Ubuntu, Debian, CentOS, Windows Server
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
          3. – На ваш email придут:<br /> <br /> 
- IP-адрес сервера<br /> <br /> 
- Логин и пароль (или SSH-ключ)<br /> <br /> 
- Ссылка на веб-панель управления<br /> <br /> 
– Можно сразу подключаться через SSH, RDP или веб-консоль
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
          4. – Установите нужное ПО (Docker, Nginx, MySQL и др.)<br /> <br /> 
– Настройте брандмауэр и безопасность<br /> <br /> 
– Загрузите файлы проекта и запускайте свои сервисы
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
          5. ServerLink обеспечивает стабильную работу без ручных настроек <br /> — просто выберите сервер и начинайте работать!
        </p>
      </div>
    </main>
  );
}

export default App;