def your_wsdl(DocumentHeader, DocumentBody):

        """Call ASIC using the SOAP API listin the BRS document

        :param DocumentHeader: dictonary with the fields as specifed in BRS documentation 
        :param DocumentBody: dictonary with the fields as specifed in BRS documentation
        """


    wsdl = Config.objects.get(code="ASIC_API").value + str('?WSDL')
    wsdl_session = Session()
    wsdl_session.auth = HTTPBasicAuth(Config.objects.get(code="ASIC_API_ID").value, Config.objects.get(code="ASIC_API_PASS").value)
    transport = Transport(session=wsdl_session)
    client = Client(wsdl, transport=transport)
    
    ##get_service2 fixes the incorrect binding response in BRS UAT
    service = get_service2(client=client)
    
    
    soap_response={}
    with client.settings(raw_response=True, xsd_ignore_sequence_order=False):
        try:
            soap_response= service.externalInitiat
        except Exception as e:
            soap_response = { 'status_code': 500 }            
            

#

def get_service2(client):

        """Fix for the incorrect Service Binding

        :param client: soap client object
        """

  # if translation:
    service_binding = client.service._binding.name
    service_address = Config.objects.get(code="ASIC_API_payment_url").value
    return client.create_service(service_binding, service_address)
