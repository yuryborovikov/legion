#!groovy
/**
 *   Copyright 2017 EPAM Systems
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 */

import jenkins.model.*
import hudson.security.*
import jenkins.security.s2m.AdminWhitelistRule
import hudson.model.*
import hudson.tools.*
import hudson.plugins.*
import hudson.security.SecurityRealm.*
import org.jenkinsci.plugins.oic.*
 
def instance = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def env = System.getenv()

if (hudsonRealm.getAllUsers().size == 0){
	hudsonRealm.createAccount("admin", "admin")
	instance.setSecurityRealm(hudsonRealm)
	 
	def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
	strategy.setAllowAnonymousRead(false)
	instance.setAuthorizationStrategy(strategy)
	instance.save()
	 
	Jenkins.instance.getInjector().getInstance(AdminWhitelistRule.class).setMasterKillSwitch(false)
}

enableOpenId = env['OPENID_ENABLE']
if (enableOpenId.toLowerCase() == "true") {
  String clientId = env['OPENID_CLIENTID']
  String clientSecret = env['OPENID_CLIENT_SECRET']
  String tokenServerUrl = env['OPENID_TOKEN_SERVER_URL']
  String authorizationServerUrl = env['OPENID_AUTH_SERVER_URL']
  String userInfoServerUrl = ''
  String userNameField = 'sub'
  String tokenFieldToCheckKey = ''
  String tokenFieldToCheckValue = ''
  String fullNameFieldName = 'name'
  String emailFieldName = 'email'
  String scopes = 'openid email profile'
  String groupsFieldName = ''
  boolean disableSslVerification = 'false'
  boolean logoutFromOpenidProvider = 'false'
  String endSessionUrl = ''
  String postLogoutRedirectUrl = ''
  boolean escapeHatchEnabled = 'false'
  String escapeHatchUsername = ''
  String escapeHatchSecret = ''
  String escapeHatchGroup = ''

  adrealm = new OicSecurityRealm(
    clientId,
    clientSecret,
    tokenServerUrl,
    authorizationServerUrl,
    userInfoServerUrl,
    userNameField,
    tokenFieldToCheckKey,
    tokenFieldToCheckValue,
    fullNameFieldName,
    emailFieldName,
    scopes,
    groupsFieldName,
    disableSslVerification,
    logoutFromOpenidProvider,
    endSessionUrl,
    postLogoutRedirectUrl,
    escapeHatchEnabled,
    escapeHatchUsername,
    escapeHatchSecret,
    escapeHatchGroup
  )

  instance.setSecurityRealm(adrealm)
  instance.save()
}

System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
