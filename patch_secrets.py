import os
import glob

workflows = glob.glob(".github/workflows/*.yml")

old_login = """      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}"""

new_login = """      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: '{"clientId":"${{ secrets.AZURE_CLIENT_ID }}","clientSecret":"${{ secrets.AZURE_CLIENT_SECRET }}","subscriptionId":"${{ secrets.AZURE_SUBSCRIPTION_ID }}","tenantId":"${{ secrets.AZURE_TENANT_ID }}"}'"""

for w in workflows:
    with open(w, 'r') as f:
        content = f.read()
    
    content = content.replace(old_login, new_login)
    
    with open(w, 'w') as f:
        f.write(content)
        
print("Updated all workflows to use 4 separate secrets.")
