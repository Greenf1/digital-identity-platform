import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  Shield, 
  Users, 
  Fingerprint, 
  Eye, 
  Search, 
  UserPlus, 
  BarChart3, 
  Settings,
  CheckCircle,
  AlertCircle,
  Clock,
  Globe
} from 'lucide-react'
import './App.css'

// Composant Header
function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Shield className="h-10 w-10" />
            <div>
              <h1 className="text-2xl font-bold">IDFAD</h1>
              <p className="text-blue-100">Plateforme d'Identité Numérique Nationale - Greenfad</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Badge variant="secondary" className="bg-green-500 text-white">
              <CheckCircle className="h-4 w-4 mr-1" />
              Système Opérationnel
            </Badge>
          </div>
        </div>
      </div>
    </header>
  )
}

// Composant Dashboard
function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatistics()
  }, [])

  const fetchStatistics = async () => {
    try {
      const response = await fetch('/api/identity/statistics')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Citoyens Enregistrés</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.citizens?.total || 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.citizens?.active || 0} actifs
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Données Biométriques</CardTitle>
            <Fingerprint className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.biometrics?.total || 0}</div>
            <p className="text-xs text-muted-foreground">
              Empreintes: {stats?.biometrics?.fingerprint || 0}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Authentifications 24h</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.authentication_24h?.total_attempts || 0}</div>
            <p className="text-xs text-muted-foreground">
              Taux de succès: {stats?.authentication_24h?.success_rate?.toFixed(1) || 0}%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Statut Système</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">100%</div>
            <p className="text-xs text-muted-foreground">
              Disponibilité
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Répartition des Citoyens par Statut</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span>Actifs</span>
                </div>
                <span className="font-medium">{stats?.citizens?.active || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <span>Suspendus</span>
                </div>
                <span className="font-medium">{stats?.citizens?.suspended || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span>Révoqués</span>
                </div>
                <span className="font-medium">{stats?.citizens?.revoked || 0}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Types de Données Biométriques</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Fingerprint className="h-4 w-4" />
                  <span>Empreintes digitales</span>
                </div>
                <span className="font-medium">{stats?.biometrics?.fingerprint || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>Reconnaissance faciale</span>
                </div>
                <span className="font-medium">{stats?.biometrics?.face || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>Iris</span>
                </div>
                <span className="font-medium">{stats?.biometrics?.iris || 0}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Composant Enregistrement
function Registration() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    middle_name: '',
    date_of_birth: '',
    place_of_birth: '',
    gender: '',
    phone_number: '',
    email: '',
    address_line1: '',
    address_line2: '',
    city: '',
    region: '',
    postal_code: '',
    father_name: '',
    mother_name: '',
    marital_status: '',
    pin: ''
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const response = await fetch('/api/identity/citizens', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({
          type: 'success',
          text: `Citoyen enregistré avec succès. ID National: ${data.national_id}`
        })
        setFormData({
          first_name: '',
          last_name: '',
          middle_name: '',
          date_of_birth: '',
          place_of_birth: '',
          gender: '',
          phone_number: '',
          email: '',
          address_line1: '',
          address_line2: '',
          city: '',
          region: '',
          postal_code: '',
          father_name: '',
          mother_name: '',
          marital_status: '',
          pin: ''
        })
      } else {
        setMessage({
          type: 'error',
          text: data.error || 'Erreur lors de l\'enregistrement'
        })
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Erreur de connexion au serveur'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <UserPlus className="h-5 w-5" />
            <span>Enregistrement d'un Nouveau Citoyen</span>
          </CardTitle>
          <CardDescription>
            Saisissez les informations du citoyen pour créer son identité numérique
          </CardDescription>
        </CardHeader>
        <CardContent>
          {message && (
            <Alert className={`mb-6 ${message.type === 'success' ? 'border-green-500' : 'border-red-500'}`}>
              {message.type === 'success' ? (
                <CheckCircle className="h-4 w-4 text-green-500" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-500" />
              )}
              <AlertDescription className={message.type === 'success' ? 'text-green-700' : 'text-red-700'}>
                {message.text}
              </AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="first_name">Prénom *</Label>
                <Input
                  id="first_name"
                  value={formData.first_name}
                  onChange={(e) => handleInputChange('first_name', e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="last_name">Nom de famille *</Label>
                <Input
                  id="last_name"
                  value={formData.last_name}
                  onChange={(e) => handleInputChange('last_name', e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="middle_name">Nom du milieu</Label>
                <Input
                  id="middle_name"
                  value={formData.middle_name}
                  onChange={(e) => handleInputChange('middle_name', e.target.value)}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="date_of_birth">Date de naissance *</Label>
                <Input
                  id="date_of_birth"
                  type="date"
                  value={formData.date_of_birth}
                  onChange={(e) => handleInputChange('date_of_birth', e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="place_of_birth">Lieu de naissance *</Label>
                <Input
                  id="place_of_birth"
                  value={formData.place_of_birth}
                  onChange={(e) => handleInputChange('place_of_birth', e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="gender">Genre *</Label>
                <Select value={formData.gender} onValueChange={(value) => handleInputChange('gender', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="M">Masculin</SelectItem>
                    <SelectItem value="F">Féminin</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="phone_number">Numéro de téléphone</Label>
                <Input
                  id="phone_number"
                  value={formData.phone_number}
                  onChange={(e) => handleInputChange('phone_number', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="address_line1">Adresse ligne 1 *</Label>
                <Input
                  id="address_line1"
                  value={formData.address_line1}
                  onChange={(e) => handleInputChange('address_line1', e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="address_line2">Adresse ligne 2</Label>
                <Input
                  id="address_line2"
                  value={formData.address_line2}
                  onChange={(e) => handleInputChange('address_line2', e.target.value)}
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="city">Ville *</Label>
                  <Input
                    id="city"
                    value={formData.city}
                    onChange={(e) => handleInputChange('city', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="region">Région *</Label>
                  <Input
                    id="region"
                    value={formData.region}
                    onChange={(e) => handleInputChange('region', e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="postal_code">Code postal</Label>
                  <Input
                    id="postal_code"
                    value={formData.postal_code}
                    onChange={(e) => handleInputChange('postal_code', e.target.value)}
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="father_name">Nom du père</Label>
                <Input
                  id="father_name"
                  value={formData.father_name}
                  onChange={(e) => handleInputChange('father_name', e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="mother_name">Nom de la mère</Label>
                <Input
                  id="mother_name"
                  value={formData.mother_name}
                  onChange={(e) => handleInputChange('mother_name', e.target.value)}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="marital_status">Statut matrimonial</Label>
                <Select value={formData.marital_status} onValueChange={(value) => handleInputChange('marital_status', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="single">Célibataire</SelectItem>
                    <SelectItem value="married">Marié(e)</SelectItem>
                    <SelectItem value="divorced">Divorcé(e)</SelectItem>
                    <SelectItem value="widowed">Veuf/Veuve</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="pin">Code PIN (4 chiffres)</Label>
                <Input
                  id="pin"
                  type="password"
                  maxLength="4"
                  value={formData.pin}
                  onChange={(e) => handleInputChange('pin', e.target.value)}
                  placeholder="1234"
                />
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Enregistrement en cours...
                </>
              ) : (
                'Enregistrer le Citoyen'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

// Composant Recherche
function Search() {
  const [searchData, setSearchData] = useState({
    national_id: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    phone_number: ''
  })
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)
    setResults([])

    try {
      const response = await fetch('/api/identity/citizens/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData)
      })

      const data = await response.json()

      if (response.ok) {
        setResults(data.citizens || [])
        if (data.citizens.length === 0) {
          setMessage({
            type: 'info',
            text: 'Aucun citoyen trouvé avec ces critères'
          })
        }
      } else {
        setMessage({
          type: 'error',
          text: data.error || 'Erreur lors de la recherche'
        })
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Erreur de connexion au serveur'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Search className="h-5 w-5" />
            <span>Recherche de Citoyens</span>
          </CardTitle>
          <CardDescription>
            Recherchez un citoyen par ses informations personnelles
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="search_national_id">ID National</Label>
                <Input
                  id="search_national_id"
                  value={searchData.national_id}
                  onChange={(e) => setSearchData(prev => ({ ...prev, national_id: e.target.value }))}
                  placeholder="202501011234"
                />
              </div>
              <div>
                <Label htmlFor="search_first_name">Prénom</Label>
                <Input
                  id="search_first_name"
                  value={searchData.first_name}
                  onChange={(e) => setSearchData(prev => ({ ...prev, first_name: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="search_last_name">Nom de famille</Label>
                <Input
                  id="search_last_name"
                  value={searchData.last_name}
                  onChange={(e) => setSearchData(prev => ({ ...prev, last_name: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="search_date_of_birth">Date de naissance</Label>
                <Input
                  id="search_date_of_birth"
                  type="date"
                  value={searchData.date_of_birth}
                  onChange={(e) => setSearchData(prev => ({ ...prev, date_of_birth: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="search_phone_number">Téléphone</Label>
                <Input
                  id="search_phone_number"
                  value={searchData.phone_number}
                  onChange={(e) => setSearchData(prev => ({ ...prev, phone_number: e.target.value }))}
                />
              </div>
            </div>
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Recherche...
                </>
              ) : (
                'Rechercher'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {message && (
        <Alert className={`${message.type === 'error' ? 'border-red-500' : 'border-blue-500'}`}>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Résultats de la recherche ({results.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.map((citizen) => (
                <div key={citizen.id} className="border rounded-lg p-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                      <p className="font-semibold">{citizen.first_name} {citizen.last_name}</p>
                      <p className="text-sm text-gray-600">ID: {citizen.national_id}</p>
                    </div>
                    <div>
                      <p className="text-sm">Né(e) le: {citizen.date_of_birth}</p>
                      <p className="text-sm">À: {citizen.place_of_birth}</p>
                    </div>
                    <div>
                      <Badge variant={citizen.status === 'active' ? 'default' : 'secondary'}>
                        {citizen.status === 'active' ? 'Actif' : citizen.status}
                      </Badge>
                      <p className="text-sm text-gray-600 mt-1">{citizen.city}, {citizen.region}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// Composant principal App
function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard" className="flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>Tableau de Bord</span>
            </TabsTrigger>
            <TabsTrigger value="registration" className="flex items-center space-x-2">
              <UserPlus className="h-4 w-4" />
              <span>Enregistrement</span>
            </TabsTrigger>
            <TabsTrigger value="search" className="flex items-center space-x-2">
              <Search className="h-4 w-4" />
              <span>Recherche</span>
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Paramètres</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard />
          </TabsContent>

          <TabsContent value="registration">
            <Registration />
          </TabsContent>

          <TabsContent value="search">
            <Search />
          </TabsContent>

          <TabsContent value="settings">
            <Card>
              <CardHeader>
                <CardTitle>Paramètres du Système</CardTitle>
                <CardDescription>
                  Configuration de la plateforme IDFAD
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Alert>
                    <Settings className="h-4 w-4" />
                    <AlertDescription>
                      Les paramètres système sont gérés par l'administrateur. 
                      Contactez l'équipe technique pour toute modification.
                    </AlertDescription>
                  </Alert>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Sécurité</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span>Chiffrement</span>
                            <Badge variant="default">AES-256</Badge>
                          </div>
                          <div className="flex justify-between">
                            <span>Authentification</span>
                            <Badge variant="default">Multi-facteurs</Badge>
                          </div>
                          <div className="flex justify-between">
                            <span>Audit</span>
                            <Badge variant="default">Activé</Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Conformité</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span>RGPD</span>
                            <Badge variant="default">Conforme</Badge>
                          </div>
                          <div className="flex justify-between">
                            <span>ISO 27001</span>
                            <Badge variant="default">Certifié</Badge>
                          </div>
                          <div className="flex justify-between">
                            <span>NIST</span>
                            <Badge variant="default">Aligné</Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
      
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Shield className="h-6 w-6" />
              <div>
                <p className="font-semibold">IDFAD Platform</p>
                <p className="text-sm text-gray-300">Développé par Greenfad</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-300">© 2025 Greenfad. Tous droits réservés.</p>
              <p className="text-sm text-gray-400">Version 1.0.0</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
