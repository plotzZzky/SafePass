import { useState, useEffect } from 'react'
import NavBar from '../elements/navbar';
import Modal from '../elements/modal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faKey, faFileCirclePlus, faFileDownload } from '@fortawesome/free-solid-svg-icons'

library.add(faPlus, faKey, faFileCirclePlus, faFileDownload)

import PwdCard from '../elements/pwdCard';


export default function App() {
    const [getToken, setToken] = useState(sessionStorage.getItem('token'));
    const [getCards, setCards] = useState("");
    const [getModalData, setModalData] = useState({});
    const [getSave, setSave] = useState(true);


    function check_login() {
        if (getToken == undefined) {
            location.href = "/SafePass/login/";
        } else {
            get_pwd()
        }
    }

    function get_pwd() {
        let url = "http://127.0.0.1:8000/pwd/"
        let data = {method: 'GET', 
                    headers: {Authorization: 'Token '+ getToken}}
        fetch(url, data)
        .then((res) => res.json())
        .then((data) =>{ 
            create_list(data['pwd'])
        })
    }

    function create_list(value) {
        setCards(
            value.length > 0
                ? value.map((data) => (
                      <PwdCard data={data} update={get_pwd} edit={() => show_edit_modal(data)}></PwdCard>
                  ))
                : []
        );
    }
    

    function show_edit_modal(data) {
        setModalData(data)
        setSave(false)
        show_modal()
    }

    function show_new_modal() {
        setModalData({})
        setSave(true)
        show_modal()
    }

    function show_modal() {
        const modal = document.getElementById("ModalNew");
        modal.classList.toggle("show");
    }

    function download() {
        let data = {method: 'GET', 
        headers: {Authorization: 'Token '+ getToken}}
        fetch('http://127.0.0.1:8000/pwd/get/', data)
        .then((response) => {
            return response.blob();
          })
          .then((blob) => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'senhas.kdbx');
            document.body.appendChild(link);
            link.click();
            window.URL.revokeObjectURL(url);
          })
    }

    useEffect(() => {
        check_login()
    }, [])


    return(
        <>
            <NavBar></NavBar>
            <div className='view-cards'>
                <div className="align-app">
                    <a onClick={show_new_modal} className='btn-app'> <FontAwesomeIcon icon="fa-solid fa-file-circle-plus" /> Nova senha</a>
                    <a onClick={download} className='btn-app'> <FontAwesomeIcon icon="fa-solid fa-file-arrow-down" /> Download </a>
                </div>
                {getCards}
            </div>
            <Modal data={getModalData} update={get_pwd} save={getSave}></Modal>
        </>
    )
}
