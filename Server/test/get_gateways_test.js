const expect = require('chai').expect;
const supertest = require('supertest');
const app = require('../worker/api');
const api = supertest(app);

describe('GET /gateways', function () {

    const gateway1 = {
        imei: 'testimei1',
        name: 'Home',
        phoneNumber: '123445'
    };

    const gateway2 = {
        imei: 'testimei2',
        name: 'Work',
        phoneNumber: '+32324234'
    };

    const user = {
        mail: 'mail@test.com',
        password: 'test',
        firstName: 'Nice',
        lastName: 'Tester'
    };


    before(function (done) {
        api.post('/v1/user')
            .set('Accept', 'application/json')
            .send(user)
            .end(function (err, res) {
                expect(res.status).to.equal(200);
                done()
            });
    });

    after(function (done) {
        api.delete(`/v1/user`)
            .auth(user.mail, user.password)
            .send()
            .expect(200, done)
    });

    beforeEach(function (done) {
        api.post('/v1/gateway')
            .set('Accept', 'application/json')
            .auth(user.mail, user.password)
            .send({imei: gateway1.imei})
            .expect(200)
            .end(function (err, res) {
                api.put(`/v1/gateway/${gateway1.imei}`)
                    .set('Accept', 'application/json')
                    .auth(user.mail, user.password)
                    .send(gateway1)
                    .expect(200)
                    .end(function (err, res) {
                        api.post('/v1/gateway')
                            .set('Accept', 'application/json')
                            .auth(user.mail, user.password)
                            .send({imei: gateway2.imei})
                            .expect(200)
                            .end(function (err, res) {
                                api.put(`/v1/gateway/${gateway2.imei}`)
                                    .set('Accept', 'application/json')
                                    .auth(user.mail, user.password)
                                    .send(gateway2)
                                    .expect(200, done)
                            })
                    })
            });
    });

    afterEach(function (done) {
        api.delete(`/v1/gateway/${gateway1.imei}`)
            .auth(user.mail, user.password)
            .send()
            .end(function (err, res) {
                expect(res.status).to.be.oneOf([200, 404]);

                api.delete(`/v1/gateway/${gateway2.imei}`)
                    .auth(user.mail, user.password)
                    .send()
                    .end(function (err, res) {
                        expect(res.status).to.be.oneOf([200, 404]);
                        done()
                    });
            });
    });

    it('should return a 200 response', function (done) {
        api.get(`/v1/gateways`)
            .set('Accept', 'application/json')
            .auth(user.mail, user.password)
            .send()
            .expect(200, done)
    });

    it('should return the gateways as list', function (done) {
        api.get(`/v1/gateways`)
            .set('Accept', 'application/json')
            .auth(user.mail, user.password)
            .send()
            .expect(200)
            .end(function (err, res) {
                expect(res.body).to.be.an('array');
                expect(res.body).to.have.lengthOf(2);
                done()
            })
    });

    it('should return a 404 response', function (done) {
        api.delete(`/v1/gateway/${gateway1.imei}`)
            .auth(user.mail, user.password)
            .send()
            .expect(200)
            .end(function (err, res) {
                api.delete(`/v1/gateway/${gateway2.imei}`)
                    .auth(user.mail, user.password)
                    .send()
                    .expect(200)
                    .end(function (err, res) {
                        api.get(`/v1/gateways`)
                            .set('Accept', 'application/json')
                            .auth(user.mail, user.password)
                            .send()
                            .expect(404)
                            .end(function (err, res) {
                                expect(res.body.errorCode).to.equal(10008);
                                done()
                            })
                    })
            });
    });

    it('should return a 401 response', function (done) {
        api.get(`/v1/gateways`)
            .set('Accept', 'application/json')
            .send()
            .expect(401, done)
    });
});
