import './App.css';
import {useEffect, useState} from 'react'
import {Route, Link} from 'react-router-dom'
import ListTweets from './components/ListTweets'
import SignUp from './components/SignUp'
import Login from './components/Login'

function App() {
  
  //TODO - add browser state check
  const [userSignedIn, setUserSignedIn] = useState(null)
  const [authToken, setAuthToken] = useState("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQzOTM2NTI0LCJpYXQiOjE2NDM5MzYyMjQsImp0aSI6IjQ3OTU1M2E5NzBhMTQzMDU5M2FkNTZjZWQ2YjAyOWY2IiwidXNlcl9pZCI6MX0.YRQ_sqHrVM6lnX1CGUOIxcBz-Y23PgUvbIn8Yd9Yy7k")

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
      
    </div>
  );
}

export default App;
