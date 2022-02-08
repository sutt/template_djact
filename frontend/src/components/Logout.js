import React, { useEffect } from 'react';
import {Link} from 'react-router-dom'

function Logout({setUserSignedIn, setAuthToken}) {
    
    useEffect(() => {
        setUserSignedIn(null)
        setAuthToken(null)
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('currentUser')
        // localStorage.clear()
    })
  
    return (
    <div>
        <h4>You have been signed out.</h4>
        <p>Back to <Link to='/'>homepage</Link></p>

    </div>
  );
}

export default Logout;
