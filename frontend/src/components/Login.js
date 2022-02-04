import React, { useState } from 'react';
import {useHistory} from 'react-router-dom'

function Login({setUserSignedIn, setAuthToken}) {
    
    // const loginEndpoint = 'mock_login'
    const loginEndpoint = 'api/token/'

    const [formInfo, setFromInfo] = useState({username:'', password:''})
    const [networkErrMsg, setNetworkErrMsg] = useState(null)
    const [clientErrMsg, setClientErrMsg] = useState(null)

    const history = useHistory()

    const statusCodeToErr = (responseObj) => {
        setNetworkErrMsg(`Network Error of code: ${responseObj.status}`)
    }

    const clientFormValidation = (formInfo) => {
        const blankFields = Object.entries(formInfo)
                                  .filter(kv => kv[1] === '')
        if (blankFields.length > 0) {
            setClientErrMsg(`${blankFields[0][0]} can not be blank`)
            return false
        }
        setClientErrMsg(null)
        return true
    }

    const handleChange = (e) => {
        setFromInfo({...formInfo, [e.target.id]: e.target.value})
    }
  
    const handleLogin = (e) => {
        
        // console.log(formInfo)
        e.preventDefault()

        setNetworkErrMsg(null)

        if (!clientFormValidation(formInfo)) {
            return
        }
        
        const apiUrl = process.env.REACT_APP_API_URL
        
        fetch( apiUrl + loginEndpoint, 
                {
                    method: 'POST',
                    headers: {
                        'Content-Type':'application/json',
                    },
                    body: JSON.stringify(formInfo)
                }
        )
            .then(res => {
                if (res.ok) {
                    return res.json()  // TODO - add try/except
                } else {
                    statusCodeToErr(res)
                    return Promise.resolve(null)
                }
            })
            .then(data => {
                if (!data) {
                    console.log(`problem with network request: ${networkErrMsg}`)
                } else {
                    
                    console.log(data)

                    if (Object.keys(data).includes('detail')) {
                        if (data.detail == "No active account found with the given credentials") {
                            setNetworkErrMsg(`username or password not correct`)
                        } else {
                            setNetworkErrMsg(`login doesn't seem to be working, response of ${JSON.stringify(data)}`)
                        }
                        
                    }

                    if (Object.keys(data).includes('access')) {
                    
                        setUserSignedIn(formInfo.username) //note: insecure method

                        setAuthToken(data.access)

                        // add tokens to localstorage here
                        
                        history.push('/')

                    } else {
                        console.log(`can't find access token. data ${JSON.stringify(data)}`)
                        setNetworkErrMsg(`json returned without a access key`)
                    }
                    
                }
            })
    }

    return (
    <div>
      <h3>Login</h3>
        <form onSubmit={handleLogin}>
            <label>username:</label>
            <input id="username" name="username" type="text" onChange={handleChange}/>
            <label>password:</label>
            <input id="password" name="username" type="text" onChange={handleChange}/>
            <button type="submit">Login</button>
        </form>
        <p>{networkErrMsg}</p>
        <p>{clientErrMsg}</p>
    </div>
    );
}

export default Login;
