const express = require('express');
const app = express();
const port = 3000;

var idDogCounter = 4;
var dogs = [
    {
      id: 1,
      name: "husky",
    },
    {
      id: 2,
      name: "pug",
    },
    {
      id: 3,
      name: "poodle",
    },
];

var idCatCounter = 4;
var cats = [
    {
      id: 1,
      name: "persa",
    },
    {
      id: 2,
      name: "siames",
    },
    {
      id: 3,
      name: "himalaia",
    },
];

app.get('/', (req, res) => res.send('Hello Pets!'));

app.get("/dogs", (req,res) => {
    if(dogs.length == 0){
        res.status(404).json({'status': 'lista vazia'});
    }else{
        res.status(200).json(dogs);
    }
});

app.get("/dog", (req,res) => {
    var dogId = req.query.id;

    if(!!!dogId){
        res.status(400).json({'erro':'id não informado'});
    }else{
        var result = dogs.find(item => item.id == dogId);

        if(result){
            res.status(200).json(result);
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.post("/dog", (req,res) => {
    var dogName = req.query.dogName;

    if(!!!dogName){
        res.status(400).json({'erro':'nome não informado'});
    }else{
        dogs.push({id: idDogCounter, name: dogName});
        idDogCounter += 1;
    
        res.status(201).json({'status': 'adicionado com sucesso'});
    }
});

app.put("/dog", (req,res) => {
    var dogId = req.query.id;
    var dogName = req.query.dogName;

    if(!!!dogId){
        res.status(400).json({'erro':'id não informado'});
    }else if(!!!dogName){
        res.status(400).json({'erro':'nome não informado'});
    }else{
        var found = false;
        
        for (var i = 0; i < dogs.length; i++) {
            if (dogs[i].id == dogId) {
                dogs[i].name = dogName;
                found = true;
                break;
            }
        }
        	
        if(found){
            res.status(200).json({'status': 'alterado com sucesso'});
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.delete("/dog", (req,res) => {
    var dogId = req.query.id;

    if(!!!dogId){
        res.status(400).json({'erro':'id não informado'});
    }else{
        var i;
        var found = false;
        for (i = 0; i < dogs.length; i++) {
            if (dogs[i].id == dogId) {
                dogs.splice(i,1);
                found = true;
                break;
            }
        }
    
        if(found){
            res.status(200).json({'status': 'excluído com sucesso'});
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.get("/cats", (req,res) => {
    if(cats.length == 0){
        res.status(404).json({'status': 'lista vazia'});
    }else{
        res.status(200).json(cats);
    }
});

app.get("/cat", (req,res) => {
    var catId = req.query.id;

    if(!!!catId){
        res.status(400).json({'erro':'id não informado'});
    }else{
        var result = cats.find(item => item.id == catId);

        if(result){
            res.status(200).json(result);
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.post("/cat", (req,res) => {
    var catName = req.query.catName;

    if(!!!catName){
        res.status(400).json({'erro':'nome não informado'});
    }else{
        cats.push({id: idCatCounter, name: catName});
        idCatCounter += 1;
    
        res.status(201).json({'status': 'adicionado com sucesso'});
    }
});

app.put("/cat", (req,res) => {
    var catId = req.query.id;
    var catName = req.query.catName;

    if(!!!catId){
        res.status(400).json({'erro':'id não informado'});
    }else if(!!!catName){
        res.status(400).json({'erro':'nome não informado'});
    }else{
        var found = false;
        
        for (var i = 0; i < cats.length; i++) {
            if (cats[i].id == catId) {
                cats[i].name = catName;
                found = true;
                break;
            }
        }
        	
        if(found){
            res.status(200).json({'status': 'alterado com sucesso'});
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.delete("/cat", (req,res) => {
    var catId = req.query.id;

    if(!!!catId){
        res.status(400).json({'erro':'id não informado'});
    }else{
        var i;
        var found = false;
        for (i = 0; i < cats.length; i++) {
            if (cats[i].id == catId) {
                cats.splice(i,1);
                found = true;
                break;
            }
        }
    
        if(found){
            res.status(200).json({'status': 'excluído com sucesso'});
        }else{
            res.status(404).json({'status': 'não encontrado'});
        }
    }
});

app.listen(port, () => console.log(`Pet app listening on port ${port}!`));

