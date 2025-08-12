#!/usr/bin/env python3
"""
Script de teste para a implementação Python da Rinha de Backend 2025
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List

class PaymentClient:
    def __init__(self, base_url: str = "http://localhost:9999"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def test_health(self) -> bool:
        """Testa o endpoint de health check"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Health check: {data}")
                return True
            else:
                print(f"[ERRO] Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERRO] Health check error: {e}")
            return False
    
    async def test_payment(self, amount: float, description: str = "Teste") -> Dict:
        """Testa o endpoint de pagamento"""
        try:
            payment_data = {
                "amount": amount,
                "description": description
            }
            
            response = await self.client.post(
                f"{self.base_url}/payments",
                json=payment_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Payment processed: {data}")
                return data
            else:
                print(f"[ERRO] Payment failed: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            print(f"[ERRO] Payment error: {e}")
            return {}
    
    async def test_summary(self) -> Dict:
        """Testa o endpoint de resumo"""
        try:
            response = await self.client.get(f"{self.base_url}/payments-summary")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Summary: {data}")
                return data
            else:
                print(f"[ERRO] Summary failed: {response.status_code}")
                return {}
        except Exception as e:
            print(f"[ERRO] Summary error: {e}")
            return {}
    
    async def stress_test(self, num_payments: int = 10) -> Dict:
        """Teste de stress com múltiplos pagamentos"""
        print(f"\n[STRESS] Iniciando teste de stress com {num_payments} pagamentos...")
        
        start_time = time.time()
        successful_payments = 0
        failed_payments = 0
        
        # Criar tarefas para pagamentos simultâneos
        tasks = []
        for i in range(num_payments):
            task = self.test_payment(100.00 + i, f"Stress test payment {i+1}")
            tasks.append(task)
        
        # Executar pagamentos em paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict) and result:
                successful_payments += 1
            else:
                failed_payments += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n[RESULTADOS] Resultados do teste de stress:")
        print(f"   [OK] Pagamentos bem-sucedidos: {successful_payments}")
        print(f"   [ERRO] Pagamentos falharam: {failed_payments}")
        print(f"   [TEMPO] Tempo total: {duration:.2f}s")
        print(f"   [THROUGHPUT] Throughput: {successful_payments/duration:.2f} pagamentos/segundo")
        
        return {
            "successful": successful_payments,
            "failed": failed_payments,
            "duration": duration,
            "throughput": successful_payments/duration if duration > 0 else 0
        }
    
    async def close(self):
        """Fecha o cliente HTTP"""
        await self.client.aclose()

async def main():
    """Função principal de teste"""
    print("[TESTE] Iniciando testes da implementação Python da Rinha de Backend 2025")
    print("=" * 60)
    
    client = PaymentClient()
    
    try:
        # Teste 1: Health check
        print("\n[1] Testando health check...")
        health_ok = await client.test_health()
        if not health_ok:
            print("[ERRO] Health check falhou. Verifique se a aplicação está rodando.")
            return
        
        # Teste 2: Pagamento simples
        print("\n[2] Testando pagamento simples...")
        payment_result = await client.test_payment(50.00, "Pagamento teste")
        if not payment_result:
            print("[ERRO] Pagamento simples falhou.")
            return
        
        # Aguardar um pouco para garantir que o pagamento foi processado
        await asyncio.sleep(1)
        
        # Teste 3: Resumo
        print("\n[3] Testando resumo de pagamentos...")
        summary_result = await client.test_summary()
        if not summary_result:
            print("[ERRO] Resumo falhou.")
            return
        
        # Teste 4: Teste de stress
        print("\n[4] Testando performance...")
        stress_result = await client.stress_test(20)
        
        # Teste 5: Pagamentos com diferentes valores
        print("\n[5] Testando diferentes valores...")
        test_amounts = [10.00, 25.50, 100.00, 500.00, 1000.00]
        for amount in test_amounts:
            await client.test_payment(amount, f"Teste valor {amount}")
            await asyncio.sleep(0.1)  # Pequena pausa entre pagamentos
        
        # Teste final: Resumo final
        print("\n[6] Resumo final...")
        final_summary = await client.test_summary()
        
        print("\n[SUCESSO] Todos os testes foram executados com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERRO] Erro durante os testes: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 