import React, {useState} from 'react';
import {useHistory} from 'react-router-dom'

function SignUp({setUserSignedIn}) {

    const signUpEndpoint = 'api/auth/signup/'

    const [formInfo, setFromInfo] = useState({username:'', password:''})
    const [networkErrMsg, setNetworkErrMsg] = useState(null)
    const [clientErrMsg, setClientErrMsg] = useState(null)

    const history = useHistory()

    const statusCodeToErr = (responseObj) => {
        const statusCode = responseObj.status
        let errorText = ''
        responseObj.text().then(text => {
            errorText = text
        
            setNetworkErrMsg(`Network Error of code: ${statusCode}` +
                             ` | response text: ${errorText}`
            )
        })
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
        
        e.preventDefault()

        const submitFormInfo = {...formInfo, email:'fake@email.com'}
        console.log(submitFormInfo)

        setNetworkErrMsg(null)
        if (!clientFormValidation(formInfo)) {
            return
        }
        
        const apiUrl = process.env.REACT_APP_API_URL
        
        fetch( apiUrl + signUpEndpoint, 
                {
                    method: 'POST',
                    headers: {
                        'Content-Type':'application/json',
                    },
                    body: JSON.stringify(submitFormInfo)
                }
        )
            .then(res => {
                if (res.ok) {
                    return res.json()
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
                    
                    // setUserSignedIn(data.username)

                    // add call to login
                    // redirect here

                    history.push('/login')
                }
            })
    }

    return (
    <div>
      <h3>Sign Up</h3>
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

export default SignUp;
