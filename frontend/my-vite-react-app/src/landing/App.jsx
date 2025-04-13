import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import myImage from './assets/uwu.svg';
import people from './assets/lol.svg';

function App() {
  const navigate = useNavigate();
  const elementsRef = useRef([]);
  const [visibleElements, setVisibleElements] = useState({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const index = elementsRef.current.indexOf(entry.target);
            if (index !== -1) {
              setVisibleElements(prev => ({
                ...prev,
                [index]: true
              }));
              observer.unobserve(entry.target);
            }
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );

    const currentElements = elementsRef.current.filter(el => el !== null && el !== undefined);
    currentElements.forEach(el => observer.observe(el));

    return () => {
      currentElements.forEach(el => observer.unobserve(el));
    };
  }, []);

  const getAnimatedStyle = (index) => {
    return {
      opacity: visibleElements[index] ? 1 : 0,
      transform: visibleElements[index] ? 'translateY(0)' : 'translateY(20px)',
      transition: 'opacity 0.6s ease-out, transform 0.6s ease-out'
    };
  };

  return (
    <main className="body">
      <div className="container">
        <div className="cub" ref={el => elementsRef.current[0] = el} style={getAnimatedStyle(0)}>
          <div id="lamp">
            <div id="top"></div>
            <div id="glass">
              {/* Левые шарики - 20 штук */}
              {[...Array(20)].map((_, index) => (
                <div 
                  key={`left-${index}`} 
                  className="bubble"
                  style={{
                    '--delay': `${Math.random() * 5}s`,
                    '--duration': `${30 + Math.random() * 20}s`,
                    '--opacity': 0.6 + Math.random() * 0.4
                  }}
                />
              ))}

              {/* Правые шарики - 20 штук */}
              {[...Array(20)].map((_, index) => (
                <div 
                  key={`right-${index}`} 
                  className="bubble-right"
                  style={{
                    '--delay': `${Math.random() * 5}s`,
                    '--duration': `${30 + Math.random() * 20}s`,
                    '--opacity': 0.6 + Math.random() * 0.4
                  }}
                />
              ))}

              {/* Центральные шарики - 3 штуки */}
              {[...Array(3)].map((_, index) => (
                <div 
                  key={`center-${index}`} 
                  className="bubble-center"
                  style={{
                    '--delay': `${Math.random() * 5}s`,
                    '--duration': `${30 + Math.random() * 20}s`,
                    '--opacity': 0.6 + Math.random() * 0.4
                  }}
                />
              ))}
            </div>
            <div id="bottom"></div>
          </div>
        </div>

        <h1 ref={el => elementsRef.current[1] = el} className="name" style={getAnimatedStyle(1)}>
          ServerLink
        </h1>

        <button
          ref={el => elementsRef.current[2] = el}
          className="log"
          style={getAnimatedStyle(2)}
          onClick={() => navigate('/login')}
        >
          зарегистрироваться / войти
        </button>

        <hr ref={el => elementsRef.current[3] = el} className="line" style={getAnimatedStyle(3)} />

        <h2 ref={el => elementsRef.current[4] = el} className="time" style={getAnimatedStyle(4)}>
          Ваше время – наш приоритет
        </h2>

        <p ref={el => elementsRef.current[5] = el} className="uwu" style={getAnimatedStyle(5)}>
          Разверните свой проект в интернете всего за несколько минут с помощью интуитивно понятной панели управления.<br /><br />
          Мы убеждены, что даже самые сложные технологии должны быть простыми в использовании. Наша задача – минимизировать рутинные настройки, чтобы вы могли сосредоточиться на развитии бизнеса.<br /><br />
          Благодаря глубокой интеграции всех сервисов, вы сможете быстро развернуть инфраструктуру для любых задач – от личного блога до высоконагруженного приложения.
        </p>

        <img
          ref={el => elementsRef.current[6] = el}
          className="setu"
          src={myImage}
          alt="Server illustration"
          style={getAnimatedStyle(6)}
          loading="lazy"
        />

        <h2 ref={el => elementsRef.current[7] = el} className="tex" style={getAnimatedStyle(7)}>
          Надежная техническая поддержка
        </h2>

        <p ref={el => elementsRef.current[8] = el} className="xz" style={getAnimatedStyle(8)}>
          Экспертная помощь Подберем оптимальное решение под ваши задачи. В большинстве случаев решаем вопросы без необходимости перехода на более дорогой тариф.<br /><br />
          Только реальные люди Никаких бездушных ботов – наши специалисты всегда на связи и готовы помочь.<br /><br />
          Мгновенная реакция Мы ценим ваше время, поэтому разместили контакты поддержки на видном месте. Обращайтесь – поможем без задержек!<br /><br />
          Гарантия оперативности С какой бы проблемой вы ни столкнулись – мы оперативно отреагируем и найдем решение.
        </p>

        <img
          ref={el => elementsRef.current[9] = el}
          className="foto"
          src={people}
          alt="Support team"
          style={getAnimatedStyle(9)}
          loading="lazy"
        />
      </div>
    </main>
  );
}

export default App;