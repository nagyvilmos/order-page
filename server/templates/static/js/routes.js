import React from "react";
import { Provider } from "react-redux";
import { HashRouter, Route, hashHistory } from "react-router-dom";
import { applyMiddleware, createStore, compose } from "redux";
import thunk from "redux-thunk";

import { persistStore, persistReducer } from "redux-persist";
import { PersistGate } from "redux-persist/integration/react";
import storage from "redux-persist/lib/storage";

import rootReducer, { initialState } from "./reducer";
import App from "./App";
// import more components

// redux-persist config
const persistConfig = {
  key: "root",
  storage,
  whitelist: ["authentication"]
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const middlewares = [thunk];

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  persistedReducer,
  initialState,
  composeEnhancers(applyMiddleware(...middlewares))
);

const persistor = persistStore(store);

export default (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <HashRouter history={hashHistory}>
        <div>
          <Route path="/" component={App} />
        </div>
      </HashRouter>
    </PersistGate>
  </Provider>
);
