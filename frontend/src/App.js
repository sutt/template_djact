import './App.css';
import {useEffect, useState} from 'react'
import {Route, Link} from 'react-router-dom'
import ListTweets from './components/ListTweets'
import SignUp from './components/SignUp'
import Login from './components/Login'
import Profile from './components/Profile'
import AuthTestMain from './components/AuthTestMain';
function App() {
  
  //TODO - add browser state check
  const [userSignedIn, setUserSignedIn] = useState(null)
  const [authToken, setAuthToken] = useState(null)

  return (
    <div className="App">
      <h1>Template App</h1>
      <nav>
        <Link to="/">Home | </Link>
        <Link to="/signup"> Sign Up | </Link>
        <Link to="/login">Login | </Link>
        <Link to="/authtest1">AuthTest1</Link>
      </nav>
      
      {userSignedIn ? (
        <nav>
          <Link to='/profile/' >
            <span>
              signed in as: {userSignedIn}
            </span>
          </Link>
        </nav>  
        ) 
        : null
      }

      <Route  exact path="/">
          <ListTweets 
            userSignedIn={userSignedIn} 
            authToken={authToken}
            />
      </Route>
      <Route  exact path="/signup">
          <SignUp 
            setUserSignedIn={setUserSignedIn} 
            setAuthToken={setAuthToken}
            />
      </Route>   
      <Route   path="/login">
          <Login 
            setUserSignedIn={setUserSignedIn} 
            setAuthToken={setAuthToken}
            />
      </Route>
      <Route   path="/profile">
          <Profile 
            userSignedIn={userSignedIn} 
            authToken={authToken}
            />
      </Route>
      <Route   path="/authtest1">
          <AuthTestMain 
            userSignedIn={userSignedIn} 
            authToken={authToken}
            />
      </Route>
    </div>
  );
}

export default App;
