import firebase

// Import
const firestoreService = require('firestore-export-import');
const firebaseConfig = require('./config.js');
const serviceAccount = require('./serviceAccount.json');

// json 파일 > 파이어스토어
const jsonToFirestore = async () => {
try {
    console.log('Initialzing Firebase');
    await firestoreService.initializeApp(serviceAccount, firebaseConfig.databaseURL);
    console.log('Firebase Initialized');

    await firestoreService.restore('./PopUpStore.json');
    console.log('Upload Success');
    }
catch (error) {
    console.log(error);
    }
};
jsonToFirestore();