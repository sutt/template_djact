import React, {useState, useEffect} from 'react';
import AuthTestCard from './AuthTestCard';

function AuthTestMain({userSignedIn, authToken}) {
 
    const testObjs = [
        {
            url: process.env.REACT_APP_API_URL + 'auth_test_one',
            endpoint: 'auth_test_one',
            method: 'GET',
            body: null,
            authToken: authToken,
        },
        {
            url: process.env.REACT_APP_API_URL + 'auth_test_one',
            endpoint: 'auth_test_one',
            method: 'POST',
            body: {user_string: 'request_body_user'},
            authToken: authToken,
        },
    ]

  
 return (
     
  <div>
      <h1>Auth Test One - Cards</h1>
      {
        testObjs.map((testObj, index) => {
            return (
                <div className="test_section" key={index}>
                    <AuthTestCard 
                        requestObj={testObj} 
                        authToken={authToken}
                    />
                </div>
            )
        })
       }
  </div>
  )
}

export default AuthTestMain;
