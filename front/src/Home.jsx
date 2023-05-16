import { useState } from 'react';
import NavBar from './elements/navbar'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faGithub } from '@fortawesome/free-brands-svg-icons'

library.add(faGithub )


export default function Home() {
    const [getToken, setToken] = useState(sessionStorage.getItem('token'));

    function to_login() {
        location.href = "/SafePass/login/"
    }

    function to_notes() {
        if (getToken == undefined) {
            location.href = "/SafePass/login/"
        } else {
            location.href = "/SafePass/notes/"
        }
    }

    return (
        <>
            <NavBar></NavBar>

            <div className='page-home'>
                <div className='brand-home'>
                    <a className='brand-home-title'> SafePass</a>
                    <div className='brand-home-slogan'>
                        Mantenha suas senhas seguras em um só lugar
                    </div>
                </div>
                <p className='home-text'> Acesse suas senhas a qualquer momento em qualquer lugar, em qualquer dispositivo, sem se preocupar com a segurança. </p>
                <button className='btn-home' onClick={to_login}> Juntar-se </button>
            </div>

            <footer>
                <a href='https://www.github.com/plotzzzky'> Dev: Plotzky <FontAwesomeIcon icon="fa-brands fa-github" /></a>
            </footer>
        </>
  )
}
