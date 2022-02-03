import './App.css';
import {useEffect, useState} from 'react'
import {Route, Link} from 'react-router-dom'
import ListTweets from './components/ListTweets'
import SignUp from './components/SignUp'
import Login from './components/Login'

function App() {
  
  //TODO - add browser state check
  const [userSignedIn, setUserSignedIn] = useState(null)

  return (
    <div className="App">
      <h1>Template App</h1>
      <nav>
        <Link to="/">Home | </Link>
        <Link to="/signup"> Sign Up | </Link>
        <Link to="/login">Login</Link>
      </nav>
      
      {userSignedIn ? (
        <nav>
          <span>signed in as: {userSignedIn}</span>
        </nav>  
        ) : null
      }

      <Route  exact path="/">
          <ListTweets userSignedIn={userSignedIn}/>
      </Route>
      <Route  exact path="/signup">
          <SignUp setUserSignedIn={setUserSignedIn} />
      </Route>   
      <Route   path="/login">
          <Login setUserSignedIn={setUserSignedIn} />
      </Route>
      
    </div>
  );
}

export default App;
