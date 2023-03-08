import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react'
import ReactDOM from 'react-dom'
import NavBar from './components/Navbar';


//new 
/**
 * 
 * 
 * 
 * import { createRoot } from 'react-dom/client';
const container = document.getElementById('app');
const root = createRoot(container); // createRoot(container!) if you use TypeScript
root.render(<App tab="home" />);
 */

//after
const App=()=>{

    return(
        <div className="container">
            <NavBar/>
        </div>
    )
}



ReactDOM.render(<App/>,document.getElementById('root'))