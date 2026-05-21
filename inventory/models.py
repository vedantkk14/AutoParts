from django.db import models


class Inventory(models.Model):

    # ── Category choices ────────────────────────────────────────────────
    class Category(models.TextChoices):
        BRAKING_SYSTEM    = 'braking',    'Braking System'
        ENGINE_COMPONENTS = 'engine',     'Engine Components'
        SUSPENSION        = 'suspension', 'Suspension'
        ELECTRICAL        = 'electrical', 'Electrical'
        OTHER             = 'other',      'Other'

    # ── Status choices ───────────────────────────────────────────────────
    class Status(models.TextChoices):
        DRAFT  = 'draft',  'Draft'
        ACTIVE = 'active', 'Active'

    # ── Brand choices ───────────────────────────────────────────────────
    class Brand(models.TextChoices):
        BOSCH       = 'bosch',        'Bosch'
        KBX         = 'kbx',          'KBX'
        MANN_FILTER = 'mann_filter',  'MANN-FILTER'
        EXIDE       = 'exide',        'Exide'
        MINDA       = 'minda',        'Minda'
        OTHER       = 'other',        'Other'


    # ── General Information ──────────────────────────────────────────────
    part_name   = models.CharField(max_length=150, verbose_name='Part Name')
    sku         = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='SKU / OEM Number',
        help_text='Stock Keeping Unit or OEM part number (e.g. BP-F-10293)',
    )
    category    = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name='Category',
    )
    brand       = models.CharField(
        max_length=100,
        choices=Brand.choices,
        verbose_name='Brand',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
    )

    # ── Inventory & Warehouse ────────────────────────────────────────────
    initial_stock        = models.PositiveIntegerField(
        default=0,
        verbose_name='Initial Stock',
    )
    low_stock_threshold  = models.PositiveIntegerField(
        default=5,
        verbose_name='Low Stock Threshold',
        help_text='A warning is triggered when stock falls below this value.',
    )
    aisle_location       = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Aisle',
        help_text='Rack / Shelf aisle identifier (e.g. A3)',
    )
    bin_location         = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Bin',
        help_text='Bin identifier within the aisle (e.g. B12)',
    )

    # ── Pricing ──────────────────────────────────────────────────────────
    wholesale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Wholesale Price (Cost)',
    )
    retail_price    = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Retail Price',
    )
    is_taxable      = models.BooleanField(
        default=False,
        verbose_name='Item is Taxable (GST applies)',
    )

    # ── Media ─────────────────────────────────────────────────────────────
    image = models.ImageField(
        upload_to='inventory/images/',
        null=True,
        blank=True,
        verbose_name='Part Image',
    )

    # ── Status & Timestamps ───────────────────────────────────────────────
    status     = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Status',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.part_name} ({self.sku})'


class VehicleCompatibility(models.Model):
    """
    Stores one compatible vehicle per row for an Inventory item.
    Linked via ForeignKey so multiple vehicles can be added
    (mirrors the 'Add Vehicle' rows in the form).
    """

    # ── Make choices ─────────────────────────────────────────────────────
    class Make(models.TextChoices):
        TOYOTA  = 'toyota',  'Toyota'
        HONDA   = 'honda',   'Honda'    
        SUZUKI  = 'maruti_suzuki',  'Maruti Suzuki'
        HYUNDAI = 'hyundai', 'Hyundai'
        KIA     = 'kia',     'Kia'
        MAHINDRA= 'mahindra','Mahindra'
        TATA    = 'tata',    'Tata'
        MG      = 'mg',    'MG'
        VOLKSWAGEN      = 'volkswagen',    'Volkswagen'
        SKODA      = 'skoda',    'Skoda'
        RENAULT      = 'Renault',    'Renault'
        NISSAN      = 'nissan',    'Nissan'
        OTHER   = 'other',   'Other'

    part       = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='vehicle_compatibilities',
        verbose_name='Inventory Item',
    )
    make       = models.CharField(
        max_length=20,
        choices=Make.choices,
        verbose_name='Make',
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name='Model',
        help_text='e.g. Camry',
    )
    year_range = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Year Range',
        help_text='e.g. 2018-2022',
    )

    class Meta:
        verbose_name        = 'Vehicle Compatibility'
        verbose_name_plural = 'Vehicle Compatibilities'

    def __str__(self):
        return f'{self.make} {self.model_name} ({self.year_range})'
