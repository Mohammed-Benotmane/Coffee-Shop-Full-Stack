export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'mohammedbenotmane', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: 'rZQV1uXEGdXl7bw7Wx0f9l3hH039ZFnP', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
