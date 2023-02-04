import {
  GET_MESSAGES_REQUEST, GET_MESSAGES_SUCCESS, GET_MESSAGES_FAILURE,
  GET_CHATS_REQUEST, GET_CHATS_SUCCESS, GET_CHATS_FAILURE
} from '../constants/ActionTypes';

const getMessagesStarted = () => ({
  type: GET_MESSAGES_REQUEST
})

const getMessagesSuccess = (messages) => ({
  type: GET_MESSAGES_SUCCESS,
  payload: messages
})

const getMessagesFailure = (errorMessage) => ({
  type: GET_MESSAGES_FAILURE,
  payload: errorMessage
})

export const getMessages = (id) => {
  return (dispatch, getState) => {
    console.log('state: ', getState())
    dispatch(getMessagesStarted())

    const localStorageMessages = JSON.parse(localStorage.getItem('messages' + id));
    if (localStorageMessages != null) {
      dispatch(getMessagesSuccess(localStorageMessages));
    } else {
      dispatch(getMessagesSuccess({ data: [], member_id: null }));
    }

    fetch('/api/chats/' + id + '/messages/', {
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:3000/',
        'Access-Control-Allow-Credentials': true
      },
      credentials: 'include'
    })
      .then(resp => resp.json())
      .then(newMessages => {
        console.log(newMessages)
        dispatch(getMessagesSuccess(newMessages))
        localStorage.setItem('messages' + id, JSON.stringify(newMessages));
      })
      .catch(err => {
        dispatch(getMessagesFailure(err.message))
      })
  }
}

const getChatsStarted = () => ({
  type: GET_CHATS_REQUEST
})

const getChatsSuccess = (chats) => ({
  type: GET_CHATS_SUCCESS,
  payload: chats
})

const getChatsFailure = (errorMessage) => ({
  type: GET_CHATS_FAILURE,
  payload: errorMessage
})

export const getChats = (id) => {
  return (dispatch, getState) => {
    console.log('state: ', getState())
    dispatch(getChatsStarted())

    const localStorageChats = JSON.parse(localStorage.getItem('chats'));
    if (localStorageChats != null) {
      dispatch(getChatsSuccess(localStorageChats));
    } else {
      dispatch(getChatsSuccess([]));
    }

    fetch('/api/chats/', {
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:3000/',
        'Access-Control-Allow-Credentials': true
      },
      credentials: 'include'
    })
      .then(resp => resp.json())
      .then(newChats => {
        console.log('adding polled data to chats state', newChats.data)
        dispatch(getChatsSuccess(newChats.data))
        localStorage.setItem('chats', JSON.stringify(newChats.data));
      })
      .catch(err => {
        dispatch(getChatsFailure(err.message))
      });
  }
}

export const getChat = (id) => {
  return (dispatch, getState) => {
    console.log('state: ', getState())
    dispatch(getChatsStarted())

    const localStorageChats = JSON.parse(localStorage.getItem('chats'));
    if (localStorageChats != null) {
      dispatch(getChatsSuccess(localStorageChats));
    } else {
      dispatch(getChatsSuccess([]));
    }

    fetch('/api/chats/' + id, {
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:3000/',
        'Access-Control-Allow-Credentials': true
      },
      credentials: 'include'
    })
      .then(resp => resp.json())
      .then(newMessages => {
        console.log(newMessages.data)
        dispatch(getChatsSuccess(newMessages.data))
        localStorage.setItem('messages' + id, JSON.stringify(newMessages.data));
      })
      .catch(err => {
        dispatch(getChatsFailure(err.message))
      })
  }
}
