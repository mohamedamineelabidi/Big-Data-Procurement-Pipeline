"""
Comprehensive Trino Testing Script
===================================
Tests Trino connectivity and query capabilities against PostgreSQL catalog

Author: Data Engineering Team
Date: January 2026
"""

from trino.dbapi import connect
from datetime import datetime


def get_trino_connection():
    """Get Trino connection"""
    return connect(
        host='localhost',
        port=8080,
        user='admin',
        catalog='postgresql',
        schema='public'
    )


def print_header(title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def test_trino_version():
    """Test 1: Check Trino version"""
    print_header("TEST 1: Trino Version")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        print(f"\n   ✅ Trino Version: {version}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_catalogs():
    """Test 2: List available catalogs"""
    print_header("TEST 2: Available Catalogs")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('SHOW CATALOGS')
        catalogs = cursor.fetchall()
        
        print("\n   Available Catalogs:")
        for catalog in catalogs:
            print(f"   • {catalog[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_schemas():
    """Test 3: List schemas in PostgreSQL catalog"""
    print_header("TEST 3: PostgreSQL Catalog Schemas")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('SHOW SCHEMAS FROM postgresql')
        schemas = cursor.fetchall()
        
        print("\n   Available Schemas:")
        for schema in schemas:
            print(f"   • {schema[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_tables():
    """Test 4: List tables in public schema"""
    print_header("TEST 4: Tables in Public Schema")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('SHOW TABLES FROM postgresql.public')
        tables = cursor.fetchall()
        
        print("\n   Available Tables:")
        for table in tables:
            print(f"   • {table[0]}")
        
        print(f"\n   ✅ Total Tables: {len(tables)}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_products_query():
    """Test 5: Query products table"""
    print_header("TEST 5: Sample Data from Products Table")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, product_name, category, price 
            FROM postgresql.public.products 
            LIMIT 5
        ''')
        
        rows = cursor.fetchall()
        
        print(f"\n   {'Product ID':<15} {'Product Name':<30} {'Category':<15} {'Price':<12}")
        print("   " + "-"*75)
        for row in rows:
            print(f"   {row[0]:<15} {row[1]:<30} {row[2]:<15} ${row[3]:<10}")
        
        print(f"\n   ✅ Successfully queried {len(rows)} products")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_suppliers_count():
    """Test 6: Count suppliers"""
    print_header("TEST 6: Suppliers Count")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM postgresql.public.suppliers')
        count = cursor.fetchone()[0]
        
        print(f"\n   ✅ Total Suppliers: {count}")
        
        # Get sample suppliers
        cursor.execute('''
            SELECT supplier_id, supplier_name, contact_email 
            FROM postgresql.public.suppliers 
            LIMIT 5
        ''')
        
        rows = cursor.fetchall()
        print(f"\n   Sample Suppliers:")
        print(f"   {'ID':<5} {'Supplier Name':<25} {'Contact Email':<30}")
        print("   " + "-"*65)
        for row in rows:
            print(f"   {row[0]:<5} {row[1]:<25} {row[2]:<30}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_replenishment_rules():
    """Test 7: Query replenishment rules"""
    print_header("TEST 7: Replenishment Rules")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, supplier_id, moq, safety_stock_level 
            FROM postgresql.public.replenishment_rules 
            LIMIT 5
        ''')
        
        rows = cursor.fetchall()
        
        print(f"\n   {'Product ID':<15} {'Supplier ID':<15} {'MOQ':<10} {'Safety Stock':<15}")
        print("   " + "-"*60)
        for row in rows:
            print(f"   {row[0]:<15} {row[1]:<15} {row[2]:<10} {row[3]:<15}")
        
        print(f"\n   ✅ Retrieved {len(rows)} replenishment rules")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_aggregate_query():
    """Test 8: Aggregate query - Products by category"""
    print_header("TEST 8: Products by Category (Aggregation)")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM postgresql.public.products 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        
        rows = cursor.fetchall()
        
        print(f"\n   {'Category':<20} {'Product Count':>15}")
        print("   " + "-"*40)
        for row in rows:
            print(f"   {row[0]:<20} {row[1]:>15}")
        
        total = sum(row[1] for row in rows)
        print("   " + "-"*40)
        print(f"   {'TOTAL':<20} {total:>15}")
        
        print(f"\n   ✅ Successfully aggregated {len(rows)} categories")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_join_query():
    """Test 9: Join query between products and suppliers"""
    print_header("TEST 9: Join Query (Products + Suppliers)")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                p.product_id,
                p.product_name,
                p.category,
                s.supplier_name,
                s.lead_time_days
            FROM postgresql.public.products p
            CROSS JOIN postgresql.public.suppliers s
            LIMIT 5
        ''')
        
        rows = cursor.fetchall()
        
        print(f"\n   {'Product ID':<15} {'Product':<25} {'Category':<15} {'Supplier':<20} {'Lead Time':<10}")
        print("   " + "-"*90)
        for row in rows:
            print(f"   {row[0]:<15} {row[1]:<25} {row[2]:<15} {row[3]:<20} {row[4]:<10}")
        
        print(f"\n   ✅ Successfully joined tables and retrieved {len(rows)} rows")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def test_complex_query():
    """Test 10: Complex analytical query"""
    print_header("TEST 10: Complex Analytical Query")
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                p.category,
                COUNT(DISTINCT p.product_id) as product_count,
                AVG(r.safety_stock_level) as avg_safety_stock,
                AVG(r.moq) as avg_moq
            FROM postgresql.public.products p
            JOIN postgresql.public.replenishment_rules r 
                ON p.product_id = r.product_id
            GROUP BY p.category
            ORDER BY product_count DESC
        ''')
        
        rows = cursor.fetchall()
        
        print(f"\n   {'Category':<15} {'Products':<12} {'Avg Safety Stock':<20} {'Avg MOQ':<15}")
        print("   " + "-"*70)
        for row in rows:
            print(f"   {row[0]:<15} {row[1]:<12} {row[2]:<20.2f} {row[3]:<15.2f}")
        
        print(f"\n   ✅ Successfully executed complex analytical query")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n   Total Tests:  {total}")
    print(f"   ✅ Passed:    {passed}")
    print(f"   ❌ Failed:    {total - passed}")
    print(f"   Pass Rate:   {pass_rate:.1f}%")
    
    if passed < total:
        print("\n   Failed Tests:")
        for test_name, result in results.items():
            if not result:
                print(f"   • {test_name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print("   🎉 ALL TRINO TESTS PASSED!")
    else:
        print(f"   ⚠️  {total - passed} test(s) failed")
    
    print("="*70 + "\n")
    
    return passed == total


def main():
    """Run all Trino tests"""
    print("\n" + "="*70)
    print("  🔍 TRINO COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {
        'Trino Version': test_trino_version(),
        'Catalogs': test_catalogs(),
        'Schemas': test_schemas(),
        'Tables': test_tables(),
        'Products Query': test_products_query(),
        'Suppliers Count': test_suppliers_count(),
        'Replenishment Rules': test_replenishment_rules(),
        'Aggregate Query': test_aggregate_query(),
        'Join Query': test_join_query(),
        'Complex Query': test_complex_query()
    }
    
    # Print summary
    success = print_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
