#!/usr/bin/env python3
import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.license_service import create_license

def main():
    parser = argparse.ArgumentParser(description='SD Inpainting Lisans Oluşturucu')
    parser.add_argument('--name', required=True, help='Müşteri adı')
    parser.add_argument('--email', required=True, help='Müşteri email adresi')
    parser.add_argument('--plan', choices=['basic', 'pro', 'enterprise'], default='basic', help='Lisans planı')
    parser.add_argument('--days', type=int, default=365, help='Lisans süresi (gün)')
    parser.add_argument('--limit', type=int, default=0, help='Kullanım limiti (0=sınırsız)')
    
    args = parser.parse_args()
    
    customer_info = {
        "name": args.name,
        "email": args.email
    }
    
    result = create_license(customer_info, args.plan, args.days, args.limit)
    
    print("\n=== Lisans Oluşturuldu ===")
    print(f"Lisans Anahtarı: {result['license_key']}")
    print(f"Müşteri: {result['license_data']['customer_name']} ({result['license_data']['customer_email']})")
    print(f"Plan: {result['license_data']['plan']}")
    print(f"Oluşturma Tarihi: {result['license_data']['creation_date']}")
    print(f"Geçerlilik Süresi: {result['license_data']['expiry_date']}")
    print(f"Kullanım Limiti: {'Sınırsız' if result['license_data']['usage_limit'] == 0 else result['license_data']['usage_limit']}")
    print("\nMüşteriye aşağıdaki lisans anahtarını iletebilirsiniz:")
    print("\n" + "="*50)
    print(f"{result['license_key']}")
    print("="*50)

if __name__ == "__main__":
    main()