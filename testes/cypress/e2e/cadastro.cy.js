Cypress.Commands.add("cadastrarUsuario", (url,username, email, senha) => {
    cy.visit(url)
    cy.get('input[name="username"]').type(username)
    cy.get('input[name="email"]').type(email)
    cy.get('input[name="senha"]').type(senha)
    cy.get('input[name="confirmar_senha"]').type(senha)
    cy.intercept('POST', url).as('finalizando_cadastro')
    cy.get('input[value="CADASTRAR"]').dblclick().wait('@finalizando_cadastro')
  })  

describe('cadastro verify',()=>{
    const url = 'http://127.0.0.1:8000/users/cadastro/'
    it('Cadastro_componentes',()=>{
        cy.visit('http://127.0.0.1:8000/')
        cy.contains('a',"Cadastre-se").click({force:true})
        cy.intercept('GET',url)
        cy.contains('h3','CADASTRO').should('be.visible')
        cy.get('input[name="username"]').should('be.visible')
        cy.get('input[name="email"]').should('be.visible')
        cy.get('input[name="senha"]').should('be.visible')
        cy.get('input[name="confirmar_senha"]').should('be.visible')
        cy.get('input[value="CADASTRAR"]').should('be.visible')
        cy.get('.logo-evento').should('be.visible')
        cy.contains('a','Já possuo uma conta').should('be.visible')
    })
    it("Cadastro_senha_fraca",()=>{
        cy.cadastrarUsuario(url,'Lima','teste@teste.com','daniel123')
        cy.contains("A senha é fraquinha: ['Esta senha é muito comum.']").should('be.visible')
    })
    it("Cadastro_email_repetido",()=>{
        it("cadastro_usuario_certo",()=>{
            cy.cadastrarUsuario(url,"Lima",'teste@teste.com','Unlock$12')

        })
        cy.cadastrarUsuario(url,"Diva",'teste@teste.com','Unlock$12')
        cy.contains('email já cadastrado').should('be.visible')

    })
    it('Cadastro_username_repetido',()=> {
        cy.cadastrarUsuario(url,"Lima",'teste1@teste.com','Unlock$12')
        cy.contains('Usuário já existente',{matchCase:false}).should('be.visible')
    })
})