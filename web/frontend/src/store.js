import { compose, createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'
import rootReducer from './reducers';

const persistConfig = {
    key: 'primary',
    storage: storage,
}
  
const persistedReducer = persistReducer(persistConfig, rootReducer)
  
const store = createStore(
    persistedReducer,
    compose(
        applyMiddleware(
            createLogger(),
        ),
    )
);

export default store;
 