describe('Login Verify', () => {
  it('login-verificando-componentes', () => {
    cy.visit('http://127.0.0.1:8000/')
    cy.contains('h3','Quer ficar rico?').should('be.visible')
    cy.contains('h3','LOGIN').should('be.visible')
    cy.contains('Username:').should('be.visible')
    cy.contains('Senha').should('be.visible')
    cy.contains('a','Cadastre-se').should('be.visible')
    cy.get('input[value="LOGAR"]').should('be.visible')
    cy.get('.logo-evento').should('be.visible')
    })
  it('login_inválido',()=>{
    cy.visit('http://127.0.0.1:8000/')
    cy.get('input[name="username"]').type('schruldwinger')
    cy.intercept('POST','http://127.0.0.1:8000/users/login').as('login')
    cy.get('input[value="LOGAR"]').click({force:true}).wait('@login')
    cy.contains('Username ou senha inválidos.').should('be.visible')
    cy.get('input[name="senha"]').type('1234')
    cy.get('input[value="LOGAR"]').dblclick().wait('@login')
    cy.contains('Username ou senha inválidos.').should('be.visible')
  })

})