import './App.css';
import {useEffect, useState} from 'react'

function App() {
  
  const url = `http://localhost:8000/tweets/`

  const [tweets, setTweets] = useState([])

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log(data)
        setTweets(data)
      })
  }, [])  
  
  return (
    <div className="App">
      
      <nav>
        <ol>
        <a href="Home">Home</a> |
        <a href="SignUp">SignUp</a> |
        <a href="Login">Login</a> |
        </ol>
      </nav>
      <h1>Auth Template: React + Django-JWT</h1>
      <ul>
      {
        tweets.map(item => {
          return (<li>{item.content}</li>)
        })
      }
      </ul>
    </div>
  );
}

export default App;
