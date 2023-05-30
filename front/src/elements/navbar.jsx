import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faLock, faUser, faBars, faHome } from '@fortawesome/free-solid-svg-icons'


import './navbar.css'

library.add(faLock, faUser, faBars, faHome)


export default function NavBar() {
  const [getToken, setToken] = useState(sessionStorage.getItem('token'));

  function OpenMenu() {
    let navbar = document.getElementsByClassName("menu")[0];
    if (navbar.className == "menu") {
      navbar.classList.add("responsive")
    } else {
      navbar.className = "menu"
    }
  }

  function go_app() {
    if (getToken == undefined) {
      location.href = "/SafePass/login/"
    } else {
      location.href = "/SafePass/app/"
    }
  }

  function go_login() {
    if (getToken == undefined) {
      location.href = "/SafePass/login/"
    }
  }

  return (
    <div className="navbar">

      <div className='navbar-align'>
        <div className="menu" id="menu">
          <a className="menu-icon" onClick={OpenMenu}>
            <FontAwesomeIcon icon="fa-solid fa-bars fa-2xl" />
          </a>

          <div className="menu-item" onClick={() => location.href = "/SafePass/"}>
            <a><FontAwesomeIcon icon="fa-solid fa-home" className='icon-Home' /> SafePass</a>
          </div>

          <div className="menu-item" onClick={go_app}>
            <a><FontAwesomeIcon icon="fa-solid fa-lock" className='icon-menu' /> Senhas</a>
          </div>

          <div className="menu-item" onClick={go_login}>
            <a><FontAwesomeIcon icon="fa-solid fa-user" className='icon-menu' /> Entrar </a>
          </div>

        </div>
      </div>
    </div>
  )
}